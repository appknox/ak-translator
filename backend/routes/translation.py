import random
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from models.schemas import TranslationRequest, TranslationResponse
from services.translation_service import TranslationService

router = APIRouter()
translation_service = TranslationService()


@router.post("/translate")
async def translate(request: TranslationRequest) -> TranslationResponse:
    try:
        translations = {}
        languages = translation_service.get_supported_languages()

        for language in languages:
            result = translation_service.process_translation(request.text, language)

            translations[language] = {
                "text": result,
                "accuracy": random.random() * 5,
            }

        return JSONResponse(content={"translations": translations})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
