import json
from typing import Dict, Any, Union, List, Tuple
from transformers import pipeline


class TranslationService:
    def __init__(self):
        # Dictionary to cache translation pipelines
        self.translators = {}

        # Language mapping for Helsinki-NLP models
        self.models = {
            "japanese": "Helsinki-NLP/opus-mt-en-jap",
            "spanish (latam)": "Helsinki-NLP/opus-mt-en-es",
            "vietnamese": "Helsinki-NLP/opus-mt-en-vi",
            "indonesian": "Helsinki-NLP/opus-mt-en-id",
        }

    def get_translator(self, target_language: str):
        """Get or create translator for specific language."""
        lang_key = target_language.lower()

        if lang_key not in self.translators:
            if lang_key not in self.models:
                raise ValueError(
                    f"Language '{target_language}' not supported. Available: {list(self.models.keys())}"
                )

            model_name = self.models[lang_key]
            print(f"Loading model: {model_name}")
            self.translators[lang_key] = pipeline("translation", model=model_name)

        return self.translators[lang_key]

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

    
    def batch_translate(
        self, strings: List[str], target_language: str, batch_size: int = 32
    ) -> List[str]:
        """Translate multiple strings in batches using transformers."""
        translator = self.get_translator(target_language)
        all_translations = []

        # Filter strings that should be translated
        translation_jobs = []
        for i, text in enumerate(strings):
            if self.should_translate(text):
                translation_jobs.append((i, text))
            else:
                translation_jobs.append((i, None))  # Mark as skip

        # Process in batches
        for i in range(0, len(translation_jobs), batch_size):
            batch_jobs = translation_jobs[i : i + batch_size]

            # Get texts that need translation
            texts_to_translate = [job[1] for job in batch_jobs if job[1] is not None]

            if texts_to_translate:
                try:
                    # Translate batch
                    results = translator(texts_to_translate)

                    # Extract translations
                    translations = [result["translation_text"] for result in results]

                    # Map back to original positions
                    translation_iter = iter(translations)
                    batch_results = []

                    for _, original_text in batch_jobs:
                        if original_text is None:
                            batch_results.append(
                                strings[len(all_translations) + len(batch_results)]
                            )
                        else:
                            batch_results.append(next(translation_iter))

                    all_translations.extend(batch_results)

                except Exception as e:
                    print(f"Batch translation failed: {e}")
                    # Fallback to individual translation
                    for _, original_text in batch_jobs:
                        if original_text is None:
                            all_translations.append(strings[len(all_translations)])
                        else:
                            all_translations.append(
                                self.translate_single(original_text, target_language)
                            )
            else:
                # No texts to translate in this batch
                for _, original_text in batch_jobs:
                    all_translations.append(strings[len(all_translations)])

        return all_translations

    def translate_single(self, text: str, target_language: str) -> str:
        """Translate single text using transformers."""
        try:
            translator = self.get_translator(target_language)
            result = translator(text)

            print({"result": result})

            return result[0]["translation_text"]

        except Exception as e:
            print(f"Translation failed for '{text}': {e}")
            return text  # Return original on failure

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

    def translate_dict(
        self, text_dict: Dict[str, Any], target_language: str
    ) -> Dict[str, Any]:
        """Dictionary translation using batch processing."""
        string_paths = self.extract_translatable_strings(text_dict)
        print(f"Found {len(string_paths)} strings to translate")

        if not string_paths:
            return text_dict

        # Get just the strings for translation
        strings_to_translate = [text for _, text in string_paths]

        # Batch translate all strings
        translated_strings = self.batch_translate(strings_to_translate, target_language)

        # Create mapping of path -> translation
        translation_map = {
            path: translation
            for (path, _), translation in zip(string_paths, translated_strings)
        }

        # Rebuild the original structure with translations
        return self.rebuild_structure(text_dict, translation_map)

    def translate(self, text: str, target_language: str) -> str:
        """Translate single text."""
        return self.translate_single(text, target_language)

    def process_translation(
        self, text: Union[str, Dict[str, Any]], target_language: str
    ):
        """Process translation for either string or dictionary input."""
        if isinstance(text, str):
            print({"text": text})
            return self.translate(text, target_language)
        else:
            return self.translate(json.dumps(text), target_language)

    def get_supported_languages(self) -> List[str]:
        """Get list of supported languages."""
        return list(self.models.keys())


# Create service instance
translation_service = TranslationService()
