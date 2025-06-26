import os
from huggingface_hub import InferenceClient
from config.settings import settings

class TranslatorServiceInferenceAPI:
    def __init__(self):
        print(os.environ["HF_TOKEN"])

        self.client = InferenceClient(
            provider="hf-inference",
            api_key=settings.HF_TOKEN,
        )

    def translate(self, text: str, model: str) -> str:
        return self.client.translation(text, model)