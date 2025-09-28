"""
API для загрузки медиафайлов
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from typing import List, Optional
from pydantic import BaseModel
from services.media_service import media_service
from auth import get_current_user
from models import User
import os
from pathlib import Path

router = APIRouter(prefix="/api/media", tags=["media"])


class MediaUploadResponse(BaseModel):
    id: str
    filename: str
    unique_filename: str
    file_type: str
    file_size: int
    url: str
    thumbnail_url: Optional[str]
    user_id: int
    created_at: str


class MediaListResponse(BaseModel):
    files: List[MediaUploadResponse]
    total: int
    page: int
    per_page: int


@router.post("/upload", response_model=MediaUploadResponse)
async def upload_file(
    file: UploadFile = File(...), current_user: User = Depends(get_current_user)
):
    """Загрузка одного файла"""
    try:
        # Читаем содержимое файла
        file_content = await file.read()

        # Проверяем файл
        is_allowed, message = media_service.is_allowed_file(
            file.filename, len(file_content)
        )
        if not is_allowed:
            raise HTTPException(status_code=400, detail=message)

        # Сохраняем файл
        file_info = await media_service.save_file(
            file_content, file.filename, current_user.id
        )

        return MediaUploadResponse(**file_info)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка загрузки файла: {str(e)}")


@router.post("/upload-multiple", response_model=List[MediaUploadResponse])
async def upload_multiple_files(
    files: List[UploadFile] = File(...), current_user: User = Depends(get_current_user)
):
    """Загрузка нескольких файлов"""
    if len(files) > 10:
        raise HTTPException(status_code=400, detail="Максимум 10 файлов за раз")

    uploaded_files = []
    errors = []

    for file in files:
        try:
            file_content = await file.read()

            is_allowed, message = media_service.is_allowed_file(
                file.filename, len(file_content)
            )
            if not is_allowed:
                errors.append(f"{file.filename}: {message}")
                continue

            file_info = await media_service.save_file(
                file_content, file.filename, current_user.id
            )
            uploaded_files.append(MediaUploadResponse(**file_info))

        except Exception as e:
            errors.append(f"{file.filename}: {str(e)}")

    if errors and not uploaded_files:
        raise HTTPException(
            status_code=400, detail=f"Ошибки загрузки: {'; '.join(errors)}"
        )

    return uploaded_files


@router.get("/files", response_model=MediaListResponse)
async def get_user_files(
    page: int = 1,
    per_page: int = 20,
    file_type: Optional[str] = None,
    current_user: User = Depends(get_current_user),
):
    """Получение списка файлов пользователя"""
    # В реальном приложении здесь будет запрос к БД
    # Пока возвращаем пустой список
    return MediaListResponse(files=[], total=0, page=page, per_page=per_page)


@router.get("/files/{file_id}")
async def get_file(file_id: str, current_user: User = Depends(get_current_user)):
    """Получение информации о файле"""
    # В реальном приложении здесь будет запрос к БД
    raise HTTPException(status_code=404, detail="Файл не найден")


@router.delete("/files/{file_id}")
async def delete_file(file_id: str, current_user: User = Depends(get_current_user)):
    """Удаление файла"""
    # В реальном приложении здесь будет запрос к БД и удаление файла
    return {"message": "Файл удален"}


@router.get("/serve/{file_path:path}")
async def serve_file(file_path: str):
    """Отдача файлов для просмотра"""
    try:
        # Безопасность: проверяем, что путь не выходит за пределы uploads
        full_path = media_service.upload_dir / file_path

        if not str(full_path).startswith(str(media_service.upload_dir)):
            raise HTTPException(status_code=403, detail="Доступ запрещен")

        if not full_path.exists():
            raise HTTPException(status_code=404, detail="Файл не найден")

        return FileResponse(full_path)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения файла: {str(e)}")


@router.get("/info/{file_path:path}")
async def get_file_info(file_path: str, current_user: User = Depends(get_current_user)):
    """Получение информации о файле"""
    try:
        file_url = f"/uploads/{file_path}"
        info = await media_service.get_file_info(file_url)

        if not info:
            raise HTTPException(status_code=404, detail="Файл не найден")

        return info

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка получения информации: {str(e)}"
        )
