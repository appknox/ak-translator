import json
from typing import Dict, Any, Union, List, Callable
from ai_agent.workflow import translator_graph
from ai_agent.state import AgentState


class TranslatorService:
    """Translator service."""

    def translate_single(
        self,
        text: str,
        target_language: str,
        is_string: bool = False,
        is_json: bool = False,
    ) -> AgentState:
        """Translate single text using langgraph."""
        res = translator_graph.execute(
            text, target_language, is_string=is_string, is_json=is_json
        )

        # Extract just the essential data
        return {
            "is_json": res["is_json"],
            "is_string": res["is_string"],
            "original_input": res["original_input_query"],
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
        translated_json = self.translate_single(
            json_string, target_language, is_json=True
        )

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
        self, data: Dict[str, Any], target_language: str, chunk_size: int = 35
    ) -> Dict[str, Any]:
        """Translate dictionary by sending chunks as JSON strings."""

        # If small enough, translate as single chunk
        if len(data) <= chunk_size:
            print("--------------------------------")
            print("data")
            print(data)
            print("--------------------------------")

            translated_json = self.translate_chunk(data, target_language)

            print("--------------------------------")
            print("translated_json")
            print(translated_json)
            print("--------------------------------")

        # Split into chunks and translate each
        chunks = self.chunk_dict(data, chunk_size)
        translated_chunks = []

        for chunk in chunks:
            print("--------------------------------")
            print("chunk")
            print(chunk)
            print("--------------------------------")

            translated_json = self.translate_chunk(
                chunk,
                target_language,
                on_chunk_failed=lambda x: translated_chunks.append(x),
            )

            translated_chunks.append(translated_json)

        # Merge all translated chunks
        print("--------------------------------")
        print("translated_chunks")
        print(translated_chunks)
        print("--------------------------------")

        result = {}

        if translated_chunks:
            # Initialize merged objects
            merged_final_translation = {}
            total_iterations = 0

            for chunk in translated_chunks:

                # update final translation and add iterations
                merged_final_translation.update(chunk["final_translation"])
                total_iterations += chunk["iterations"]

                # Take single values from last chunk
                result["is_json"] = chunk["is_json"]
                result["is_string"] = chunk["is_string"]
                result["target_language"] = chunk["target_language"]
                result["translation_rating"] = chunk["translation_rating"]
                result["review_decision"] = chunk["review_decision"]
                result["review_reasoning"] = chunk["review_reasoning"]

            result["original_input"] = data
            result["iterations"] = total_iterations
            result["final_translation"] = merged_final_translation

        return result

    def process_translation(
        self,
        text: Union[str, Dict[str, Any]],
        target_language: str,
        chunk_size: int = 40,
    ):
        """Process translation for either string or dictionary input."""

        try:
            json_data = json.loads(text)
            return self.translate_dict_batched(json_data, target_language, chunk_size)
        except json.JSONDecodeError:
            return self.translate_single(text, target_language, is_string=True)


# Create service instance
translator_service = TranslatorService()
