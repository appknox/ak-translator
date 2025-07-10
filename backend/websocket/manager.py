import logging
import json

from typing import Dict, Any, Optional
from fastapi import WebSocket

logger = logging.getLogger(__name__)


class WebSocketManager:
    def __init__(self):
        self.connections: Dict[str, WebSocket] = {}

    def connect(self, client_id: str, websocket: WebSocket):
        """Add a new WebSocket connection."""
        self.connections[client_id] = websocket

        logger.info(
            f"Client {client_id} connected. Total connections: {len(self.connections)}"
        )

    def disconnect(self, client_id: str):
        """Remove WebSocket connection."""
        if client_id in self.connections:
            del self.connections[client_id]

            logger.info(
                f"Client {client_id} disconnected. Total connections: {len(self.connections)}"
            )

    async def send_to_client(self, client_id: str, message: Dict[str, Any]):
        """Send message to specific client."""
        if client_id in self.connections:
            try:
                logger.info(f"Sending message to {client_id}: {message}")
                await self.connections[client_id].send_text(json.dumps(message))
                return True

            except Exception as e:
                logger.error(f"Failed to send to {client_id}: {e}")
                self.disconnect(client_id)

                return False
        return False

    def broadcast(self, message: Dict[str, Any], exclude_client: Optional[str] = None):
        """Send message to all connected clients."""
        failed_clients = []

        for client_id, websocket in self.connections.items():
            if client_id != exclude_client:
                try:
                    websocket.send_json(message)

                except Exception as e:
                    logger.error(f"Failed to broadcast to {client_id}: {e}")
                    failed_clients.append(client_id)

        # Clean up failed connections
        for client_id in failed_clients:
            self.disconnect(client_id)

    def get_connection_count(self) -> int:
        """Get number of active connections."""
        return len(self.connections)

    def get_connected_clients(self) -> list:
        """Get list of connected client IDs."""
        return list(self.connections.keys())


ws_manager = WebSocketManager()
