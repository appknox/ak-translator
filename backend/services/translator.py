import json
from typing import Dict, Any, Union, List, Callable
from ai_agent.workflow import translator_graph
from ai_agent.state import TranslationAgentState, QueryAssessmentState


class TranslatorService:
    """Translator service."""

    def __init__(self):
        # Add cache to avoid re-evaluating the same content after first language translation
        self.content_cache = {
            "original_input_content": "",
            "translated_json": {},
            "text_was_transformed_to_json": False,
        }

    def perform_query_assessment(
        self, text: str, target_language: str
    ) -> QueryAssessmentState:
        """Perform query assessment to determine if the content should be translated as a JSON object or a string."""
        assessment_state = translator_graph.execute_query_assessment(input_query=text)
        fixed_json_state = (
            assessment_state["fixed_json_state"]
            if "fixed_json_state" in assessment_state
            else None
        )

        text_was_transformed_to_json = fixed_json_state and (
            fixed_json_state.content_was_fixed
            or (len(fixed_json_state.fixed_json_content) > 0)
        )

        # If the content was transformed to a JSON object, translate the JSON object
        if text_was_transformed_to_json:
            print("--------------------------------")
            print("fixed_json_state.fixed_json_content")
            print(fixed_json_state.fixed_json_content)
            print("--------------------------------")

            self.content_cache["text_was_transformed_to_json"] = True
            self.content_cache["translated_json"] = fixed_json_state.fixed_json_content
            self.content_cache["original_input_content"] = text

            result = self.translate_dict_batched(
                data=fixed_json_state.fixed_json_content,
                target_language=target_language,
            )

            return result

        # If the content was not transformed to a JSON object, translate the string
        return self.translate_single(text, target_language)

    def translate_single(
        self,
        text: str,
        target_language: str,
    ) -> TranslationAgentState:
        """Translate single text using langgraph."""
        res = translator_graph.execute_translation(
            input_query=text, target_language=target_language
        )

        # Extract just the essential data
        return {
            "original_input": res["input_query"],
            "target_language": res["target_language"],
            "final_translation": res["format_state"].final_translation,
            "translation_rating": res["format_state"].final_translation_rating,
            "review_decision": res["review_state"].review_decision,
            "review_reasoning": res["review_state"].review_reasoning,
            "iterations": res["translation_state"].iteration,
        }

    def chunk_dict(
        self, data: Dict[str, Any], chunk_size: int = 40
    ) -> List[Dict[str, Any]]:
        """Split dictionary into chunks of specified size."""

        items = list(data.items())
        chunks = []

        for i in range(0, len(items), chunk_size):
            chunk_items = items[i : i + chunk_size]
            chunks.append(dict(chunk_items))

        return chunks

    def translate_chunk(
        self,
        chunk: Dict[str, Any],
        target_language: str,
        on_chunk_translated: Callable[[Dict[str, Any]], None] = lambda x: None,
        on_chunk_failed: Callable[[Dict[str, Any]], None] = lambda x: None,
    ) -> Dict[str, Any]:
        """Translate a chunk of data."""
        json_string = json.dumps(chunk, ensure_ascii=False, indent=2)
        translated_json = self.translate_single(json_string, target_language)

        try:
            if isinstance(translated_json, str):
                translated_chunk = json.loads(translated_json)
                on_chunk_translated(translated_chunk)

                return translated_chunk
            else:
                on_chunk_translated(translated_json)
                return translated_json

        except (json.JSONDecodeError, Exception) as e:
            print(f"Failed to translate chunk: {e}")
            on_chunk_failed(chunk)

    def translate_dict_batched(
        self,
        data: Union[Dict[str, Any], List[Any]],
        target_language: str,
        chunk_size: int = 40,
    ) -> Dict[str, Any]:
        """Translate dictionary by sending chunks as JSON strings."""

        if isinstance(data, list):
            return self.translate_single(data, target_language)

        # Split into chunks and translate each
        chunks = self.chunk_dict(data, chunk_size)
        translated_chunks = []

        for chunk in chunks:
            translated_json = self.translate_chunk(
                chunk,
                target_language,
                on_chunk_failed=lambda x: translated_chunks.append(x),
            )

            translated_chunks.append(translated_json)

        # Merge all translated chunks
        translated_chunks_length = len(translated_chunks)
        result = translated_chunks[0] if translated_chunks_length > 0 else {}

        if translated_chunks_length > 1:
            # Initialize merged objects
            merged_final_translation = {}
            total_iterations = 0

            for chunk in translated_chunks:

                # update final translation and add iterations
                merged_final_translation.update(chunk["final_translation"])
                total_iterations += chunk["iterations"]

                # Take single values from last chunk
                result["target_language"] = chunk["target_language"]
                result["translation_rating"] = chunk["translation_rating"]
                result["review_decision"] = chunk["review_decision"]
                result["review_reasoning"] = chunk["review_reasoning"]

            result["original_input"] = data
            result["iterations"] = total_iterations
            result["final_translation"] = merged_final_translation

        return result

    def reset_cache(self, reset_cache: bool = False):
        """Reset the content cache after last translation."""
        if reset_cache:
            print("--------------------------------")
            print("cache reset")
            print("--------------------------------")

            self.content_cache = {
                "original_input_content": "",
                "translated_json": {},
                "text_was_transformed_to_json": False,
            }

    def process_translation(
        self,
        text: Union[str, Dict[str, Any]],
        target_language: str,
        reset_cache: bool = False,
    ):
        """Process translation for either string or dictionary input."""

        # If the same content is being translated to another language,
        # use the cached translated JSON if available
        if (
            self.content_cache["original_input_content"] == text
            and self.content_cache["text_was_transformed_to_json"]
        ):
            text = json.dumps(self.content_cache["translated_json"])

        # If the content is a JSON object, translate the JSON object
        try:
            json_data = json.loads(text)
            result = self.translate_dict_batched(json_data, target_language)
            self.reset_cache(reset_cache=reset_cache)

            return result

        # If the content is not a JSON object, perform query assessment
        except json.JSONDecodeError:
            result = self.perform_query_assessment(text, target_language)
            self.reset_cache(reset_cache=reset_cache)

            return result


# Create service instance
translator_service = TranslatorService()
