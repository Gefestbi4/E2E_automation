"""
WebSocket Manager - управление WebSocket соединениями
"""

import json
import asyncio
from typing import Dict, List, Any
from fastapi import WebSocket, WebSocketDisconnect
import logging

logger = logging.getLogger(__name__)


class WebSocketManager:
    """Менеджер WebSocket соединений"""

    def __init__(self):
        # Активные соединения
        self.active_connections: List[WebSocket] = []
        # Соединения по пользователям
        self.user_connections: Dict[str, List[WebSocket]] = {}
        # Подписки на события
        self.subscriptions: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_id: str = None):
        """Подключение нового WebSocket клиента"""
        await websocket.accept()
        self.active_connections.append(websocket)

        if user_id:
            if user_id not in self.user_connections:
                self.user_connections[user_id] = []
            self.user_connections[user_id].append(websocket)

        logger.info(
            f"WebSocket connected. Total connections: {len(self.active_connections)}"
        )

        # Отправляем приветственное сообщение
        await self.send_personal_message(
            {
                "type": "connection",
                "message": "Connected to real-time updates",
                "timestamp": asyncio.get_event_loop().time(),
            },
            websocket,
        )

    def disconnect(self, websocket: WebSocket, user_id: str = None):
        """Отключение WebSocket клиента"""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

        if user_id and user_id in self.user_connections:
            if websocket in self.user_connections[user_id]:
                self.user_connections[user_id].remove(websocket)
            if not self.user_connections[user_id]:
                del self.user_connections[user_id]

        # Удаляем из всех подписок
        for event_type, connections in self.subscriptions.items():
            if websocket in connections:
                connections.remove(websocket)

        logger.info(
            f"WebSocket disconnected. Total connections: {len(self.active_connections)}"
        )

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """Отправка сообщения конкретному клиенту"""
        try:
            await websocket.send_text(json.dumps(message))
        except Exception as e:
            logger.error(f"Error sending personal message: {e}")

    async def send_to_user(self, message: dict, user_id: str):
        """Отправка сообщения всем соединениям пользователя"""
        if user_id in self.user_connections:
            for websocket in self.user_connections[user_id]:
                await self.send_personal_message(message, websocket)

    async def broadcast(self, message: dict):
        """Отправка сообщения всем подключенным клиентам"""
        for websocket in self.active_connections:
            await self.send_personal_message(message, websocket)

    async def send_to_subscribers(self, event_type: str, message: dict):
        """Отправка сообщения подписчикам на определенный тип событий"""
        if event_type in self.subscriptions:
            for websocket in self.subscriptions[event_type]:
                await self.send_personal_message(message, websocket)

    def subscribe(self, websocket: WebSocket, event_type: str):
        """Подписка на тип событий"""
        if event_type not in self.subscriptions:
            self.subscriptions[event_type] = []
        if websocket not in self.subscriptions[event_type]:
            self.subscriptions[event_type].append(websocket)

    def unsubscribe(self, websocket: WebSocket, event_type: str):
        """Отписка от типа событий"""
        if event_type in self.subscriptions:
            if websocket in self.subscriptions[event_type]:
                self.subscriptions[event_type].remove(websocket)

    async def handle_message(self, websocket: WebSocket, message: str):
        """Обработка входящих сообщений от клиента"""
        try:
            data = json.loads(message)
            message_type = data.get("type")

            if message_type == "subscribe":
                event_type = data.get("event_type")
                if event_type:
                    self.subscribe(websocket, event_type)
                    await self.send_personal_message(
                        {
                            "type": "subscription_confirmed",
                            "event_type": event_type,
                            "message": f"Subscribed to {event_type} events",
                        },
                        websocket,
                    )

            elif message_type == "unsubscribe":
                event_type = data.get("event_type")
                if event_type:
                    self.unsubscribe(websocket, event_type)
                    await self.send_personal_message(
                        {
                            "type": "unsubscription_confirmed",
                            "event_type": event_type,
                            "message": f"Unsubscribed from {event_type} events",
                        },
                        websocket,
                    )

            elif message_type == "ping":
                await self.send_personal_message(
                    {"type": "pong", "timestamp": asyncio.get_event_loop().time()},
                    websocket,
                )

            else:
                await self.send_personal_message(
                    {
                        "type": "error",
                        "message": f"Unknown message type: {message_type}",
                    },
                    websocket,
                )

        except json.JSONDecodeError:
            await self.send_personal_message(
                {"type": "error", "message": "Invalid JSON format"}, websocket
            )
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            await self.send_personal_message(
                {"type": "error", "message": "Internal server error"}, websocket
            )


# Глобальный экземпляр менеджера
websocket_manager = WebSocketManager()
