from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from models.schemas import TranslationRequest, TranslationResponse
from config.constants import SUPPORTED_LANGUAGES
from services.translator import translator_service

router = APIRouter()


@router.post("/translate")
async def translate(request: TranslationRequest) -> TranslationResponse:
    try:
        translations = {}

        for language in SUPPORTED_LANGUAGES:
            result = translator_service.process_translation(request.text, language)
            translations[language] = result

        return JSONResponse(content={"translations": translations})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
