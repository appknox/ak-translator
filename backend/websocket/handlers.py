import asyncio
from typing import Any, Dict, List

from websocket.manager import ws_manager
from services.translator import translator_service
from config.constants import SUPPORTED_LANGUAGES


async def handle_websocket_message(client_id: str, message: Dict[str, Any]):
    """Handle incoming WebSocket messages."""
    msg_type = message.get("type")

    if msg_type == "translate_multi":
        await handle_multi_translation_request(client_id, message)

    elif msg_type == "ping":
        await ws_manager.send_to_client(client_id, {"type": "pong"})


async def handle_multi_translation_request(client_id: str, message: Dict[str, Any]):
    """Handle multi-language translation request."""
    try:
        text = message.get("text", "")
        target_languages = SUPPORTED_LANGUAGES

        job_id = message.get(
            "job_id", f"job_{client_id}_{asyncio.get_event_loop().time()}"
        )

        if not target_languages:
            await ws_manager.send_to_client(
                client_id,
                {"type": "translation_error", "error": "No target languages specified"},
            )
            return

        # Send job started
        await ws_manager.send_to_client(
            client_id,
            {
                "type": "multi_translation_started",
                "job_id": job_id,
                "total_languages": len(target_languages),
                "languages": target_languages,
            },
        )

        # Start translations for all languages concurrently
        tasks = []

        for language in target_languages:
            task = asyncio.create_task(
                translate_single_language(
                    client_id, job_id, text, language, target_languages
                )
            )
            tasks.append(task)

        # Wait for all translations to complete
        await asyncio.gather(*tasks, return_exceptions=True)

        # Send completion message
        await ws_manager.send_to_client(
            client_id, {"type": "multi_translation_completed", "job_id": job_id}
        )

    except Exception as e:
        await ws_manager.send_to_client(
            client_id, {"type": "translation_error", "job_id": job_id, "error": str(e)}
        )


async def translate_single_language(
    client_id: str, job_id: str, text: str, language: str, all_languages: List[str]
):
    """Translate text to a single language and send result immediately."""
    try:
        # Send progress for this language
        await ws_manager.send_to_client(
            client_id,
            {
                "type": "language_translation_started",
                "job_id": job_id,
                "language": language,
                "progress": f"Translating to {language}...",
            },
        )

        # Perform translation
        result = translator_service.process_translation(text, language)

        # Send completed translation immediately
        await ws_manager.send_to_client(
            client_id,
            {
                "type": "language_translation_completed",
                "job_id": job_id,
                "language": language,
                "original_text": text,
                "translated_text": result,
                "completed_count": len(
                    [lang for lang in all_languages if lang == language]
                ),
                "total_count": len(all_languages),
            },
        )

    except Exception as e:
        await ws_manager.send_to_client(
            client_id,
            {
                "type": "language_translation_failed",
                "job_id": job_id,
                "language": language,
                "error": str(e),
            },
        )
