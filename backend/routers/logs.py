"""
API endpoints для логгирования фронтенда
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from auth import get_db
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import json

router = APIRouter()


class LogEntry(BaseModel):
    """Схема лог-записи от фронтенда"""

    timestamp: str
    level: str
    category: str
    message: str
    data: Optional[dict] = None
    url: str
    user_agent: str
    session_id: str


class LogFilter(BaseModel):
    """Схема фильтра логов"""

    level: Optional[str] = None
    category: Optional[str] = None
    since: Optional[str] = None
    session_id: Optional[str] = None


@router.post("/api/logs")
async def create_log(log_entry: LogEntry, db: Session = Depends(get_db)):
    """Создание новой лог-записи"""
    try:
        # В реальном приложении здесь была бы запись в БД
        # Пока что просто логируем в консоль
        print(
            f"📝 Frontend Log [{log_entry.level.upper()}] {log_entry.category}: {log_entry.message}"
        )
        if log_entry.data:
            print(f"   Data: {json.dumps(log_entry.data, indent=2)}")

        return {"status": "success", "message": "Log entry created"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to create log entry: {str(e)}"
        )


@router.get("/api/logs")
async def get_logs(
    level: Optional[str] = None,
    category: Optional[str] = None,
    since: Optional[str] = None,
    session_id: Optional[str] = None,
    limit: int = 100,
):
    """Получение логов с фильтрацией"""
    try:
        # В реальном приложении здесь был бы запрос к БД
        # Пока что возвращаем заглушку
        logs = [
            {
                "timestamp": datetime.now().isoformat(),
                "level": "info",
                "category": "API",
                "message": "Logs endpoint accessed",
                "data": {
                    "filters": {
                        "level": level,
                        "category": category,
                        "since": since,
                        "session_id": session_id,
                    }
                },
                "url": "http://localhost:8000/api/logs",
                "user_agent": "Logger/1.0",
                "session_id": session_id or "unknown",
            }
        ]

        return {
            "status": "success",
            "data": logs,
            "total": len(logs),
            "filters": {
                "level": level,
                "category": category,
                "since": since,
                "session_id": session_id,
            },
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get logs: {str(e)}")


@router.delete("/api/logs")
async def clear_logs():
    """Очистка всех логов"""
    try:
        # В реальном приложении здесь была бы очистка БД
        return {"status": "success", "message": "Logs cleared"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to clear logs: {str(e)}")


@router.get("/api/logs/stats")
async def get_log_stats():
    """Получение статистики логов"""
    try:
        # В реальном приложении здесь была бы аналитика логов
        stats = {
            "total_logs": 0,
            "errors_count": 0,
            "warnings_count": 0,
            "info_count": 0,
            "debug_count": 0,
            "unique_sessions": 0,
            "most_common_categories": [],
            "recent_errors": [],
        }

        return {"status": "success", "data": stats}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get log stats: {str(e)}"
        )
