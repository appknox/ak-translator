from typing import Dict, Union
from pydantic import BaseModel


class TranslationRequest(BaseModel):
    text: Union[str, Dict[str, str]]


class TranslationResult(BaseModel):
    text: Union[str, Dict[str, str]]
    accuracy: float


class TranslationResponse(BaseModel):
    translations: Dict[str, TranslationResult]
