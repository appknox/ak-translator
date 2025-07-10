from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import WebSocket, WebSocketDisconnect

from config.settings import settings
from routes.translation import router
from websocket.manager import ws_manager
from websocket.handlers import handle_websocket_message

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router, tags=["translation"])


# WebSocket endpoint
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    """WebSocket endpoint for real-time translations."""
    await websocket.accept()
    ws_manager.connect(client_id, websocket)

    try:
        while True:
            message = await websocket.receive_json()
            await handle_websocket_message(client_id, message)

    except WebSocketDisconnect:
        ws_manager.disconnect(client_id)

    except Exception as e:
        print(f"WebSocket error for {client_id}: {e}")
        ws_manager.disconnect(client_id)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
