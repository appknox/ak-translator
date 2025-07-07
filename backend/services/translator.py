import asyncio
import concurrent.futures

from typing import Dict, Any, Union, List, Tuple
from langchain_core.messages import HumanMessage
from translator_graph.nodes import translator_graph


class TranslatorService:

    async def _translate_batch_async(
        self, batch: List[str], target_language: str
    ) -> List[str]:
        """Translate a single batch asynchronously."""
        loop = asyncio.get_event_loop()

        # Run the blocking transformer call in a thread pool
        with concurrent.futures.ThreadPoolExecutor() as executor:
            translator = await loop.run_in_executor(
                executor, self.get_translator, target_language
            )

            results = await loop.run_in_executor(executor, translator, batch)

        print(f"Translated {len(results)} strings")

        return [result["translation_text"] for result in results]

    async def batch_translate(
        self, strings: List[str], target_language: str, batch_size: int = 32
    ) -> List[str]:
        """Translate multiple strings in batches asynchronously."""

        # Create batches
        batches = [
            strings[i : i + batch_size] for i in range(0, len(strings), batch_size)
        ]

        # Run all batches concurrently
        tasks = [
            self._translate_batch_async(batch, target_language) for batch in batches
        ]

        batch_results = await asyncio.gather(*tasks, return_exceptions=True)

        # Flatten results
        all_translations = []

        for result in batch_results:
            if isinstance(result, Exception):
                print(f"Batch failed: {result}")
                # Add empty results for failed batch
                all_translations.extend([""] * batch_size)
            else:
                all_translations.extend(result)

        return all_translations[: len(strings)]  # Trim to original length

    def translate_single(self, text: str, target_language: str) -> str:
        """Translate single text using langgraph."""

        inputs = [
            HumanMessage(
                content=f"""
                    Can you translate only the text below into {target_language}? 
                    NOTE: Only output the translation, no other text.

                    ==================
                    {text}
                    ==================
                """
            )
        ]

        res = translator_graph.invoke(inputs)
        translation = res[-1].content

        return translation

    def rebuild_structure(
        self, original_data: Dict[str, Any], translations: Dict[str, str]
    ) -> Dict[str, Any]:
        """Rebuild the original structure with translations."""

        def rebuild_recursive(obj, path=""):
            if isinstance(obj, str):
                return translations.get(path, obj)

            elif isinstance(obj, dict):
                result = {}

                for key, value in obj.items():
                    new_path = f"{path}.{key}" if path else key
                    result[key] = rebuild_recursive(value, new_path)

                return result

            elif isinstance(obj, list):
                result = []
                for i, item in enumerate(obj):
                    new_path = f"{path}[{i}]"
                    result.append(rebuild_recursive(item, new_path))

                return result

            else:
                return obj

        return rebuild_recursive(original_data)

    async def translate_dict(
        self, text_dict: Dict[str, Any], target_language: str
    ) -> Dict[str, Any]:
        """Dictionary translation using batch processing."""
        string_paths = self.extract_translatable_strings(text_dict)

        if not string_paths:
            return text_dict

        # Get just the strings for translation
        strings_to_translate = [text for _, text in string_paths]

        # Batch translate all strings
        translated_strings = await self.batch_translate(
            strings_to_translate, target_language
        )

        # Create mapping of path -> translation
        translation_map = {
            path: translation
            for (path, _), translation in zip(string_paths, translated_strings)
        }

        # Rebuild the original structure with translations
        return self.rebuild_structure(text_dict, translation_map)

    def extract_translatable_strings(
        self, data: Dict[str, Any], path: str = ""
    ) -> List[Tuple[str, str]]:
        """Extract all translatable strings with their paths."""
        strings_to_translate = []

        def extract_recursive(obj, current_path):
            if isinstance(obj, str):
                strings_to_translate.append((current_path, obj))

            elif isinstance(obj, dict):
                for key, value in obj.items():
                    new_path = f"{current_path}.{key}" if current_path else key
                    extract_recursive(value, new_path)

            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    new_path = f"{current_path}[{i}]"
                    extract_recursive(item, new_path)

        extract_recursive(data, path)
        return strings_to_translate

    def process_translation(
        self, text: Union[str, Dict[str, Any]], target_language: str
    ):
        """Process translation for either string or dictionary input."""

        if isinstance(text, str):
            return self.translate_single(text, target_language)
        else:
            return self.translate_dict(text, target_language)


# Create service instance
translator_service = TranslatorService()
