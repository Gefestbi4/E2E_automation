"""
Сервис для работы с медиафайлами
"""

import os
import uuid
import aiofiles
from typing import List, Dict, Optional, Tuple
from PIL import Image
import logging
from pathlib import Path
import mimetypes

logger = logging.getLogger(__name__)


class MediaService:
    """Сервис для обработки медиафайлов"""

    def __init__(self):
        self.upload_dir = Path("uploads")
        self.upload_dir.mkdir(exist_ok=True)

        # Создаем подпапки
        (self.upload_dir / "images").mkdir(exist_ok=True)
        (self.upload_dir / "videos").mkdir(exist_ok=True)
        (self.upload_dir / "documents").mkdir(exist_ok=True)
        (self.upload_dir / "thumbnails").mkdir(exist_ok=True)

        # Поддерживаемые форматы
        self.allowed_image_types = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"}
        self.allowed_video_types = {".mp4", ".avi", ".mov", ".wmv", ".flv", ".webm"}
        self.allowed_document_types = {".pdf", ".doc", ".docx", ".txt", ".rtf"}

        # Максимальные размеры файлов (в байтах)
        self.max_file_size = 50 * 1024 * 1024  # 50MB
        self.max_image_size = 10 * 1024 * 1024  # 10MB
        self.max_video_size = 100 * 1024 * 1024  # 100MB

    def get_file_type(self, filename: str) -> str:
        """Определяет тип файла по расширению"""
        ext = Path(filename).suffix.lower()

        if ext in self.allowed_image_types:
            return "image"
        elif ext in self.allowed_video_types:
            return "video"
        elif ext in self.allowed_document_types:
            return "document"
        else:
            return "unknown"

    def is_allowed_file(self, filename: str, file_size: int) -> Tuple[bool, str]:
        """Проверяет, разрешен ли файл для загрузки"""
        file_type = self.get_file_type(filename)

        if file_type == "unknown":
            return False, "Неподдерживаемый формат файла"

        if file_size > self.max_file_size:
            return (
                False,
                f"Файл слишком большой. Максимум: {self.max_file_size // (1024*1024)}MB",
            )

        if file_type == "image" and file_size > self.max_image_size:
            return (
                False,
                f"Изображение слишком большое. Максимум: {self.max_image_size // (1024*1024)}MB",
            )

        if file_type == "video" and file_size > self.max_video_size:
            return (
                False,
                f"Видео слишком большое. Максимум: {self.max_video_size // (1024*1024)}MB",
            )

        return True, "OK"

    async def save_file(self, file_content: bytes, filename: str, user_id: int) -> Dict:
        """Сохраняет файл на диск"""
        try:
            # Генерируем уникальное имя файла
            file_ext = Path(filename).suffix.lower()
            unique_filename = f"{uuid.uuid4()}{file_ext}"

            # Определяем тип файла и папку
            file_type = self.get_file_type(filename)
            if file_type == "image":
                folder = "images"
            elif file_type == "video":
                folder = "videos"
            elif file_type == "document":
                folder = "documents"
            else:
                folder = "documents"

            # Путь для сохранения
            file_path = self.upload_dir / folder / unique_filename

            # Сохраняем файл
            async with aiofiles.open(file_path, "wb") as f:
                await f.write(file_content)

            # Создаем миниатюру для изображений
            thumbnail_url = None
            if file_type == "image":
                thumbnail_url = await self.create_thumbnail(file_path, unique_filename)

            # Возвращаем информацию о файле
            return {
                "id": str(uuid.uuid4()),
                "filename": filename,
                "unique_filename": unique_filename,
                "file_type": file_type,
                "file_size": len(file_content),
                "url": f"/uploads/{folder}/{unique_filename}",
                "thumbnail_url": thumbnail_url,
                "user_id": user_id,
                "created_at": "2025-01-28T10:00:00Z",  # В реальном приложении использовать datetime.now()
            }

        except Exception as e:
            logger.error(f"Error saving file {filename}: {e}")
            raise Exception(f"Ошибка сохранения файла: {str(e)}")

    async def create_thumbnail(self, image_path: Path, filename: str) -> str:
        """Создает миниатюру для изображения"""
        try:
            # Открываем изображение
            with Image.open(image_path) as img:
                # Конвертируем в RGB если нужно
                if img.mode in ("RGBA", "LA", "P"):
                    img = img.convert("RGB")

                # Создаем миниатюру
                img.thumbnail((300, 300), Image.Resampling.LANCZOS)

                # Сохраняем миниатюру
                thumbnail_filename = f"thumb_{filename}"
                thumbnail_path = self.upload_dir / "thumbnails" / thumbnail_filename
                img.save(thumbnail_path, "JPEG", quality=85)

                return f"/uploads/thumbnails/{thumbnail_filename}"

        except Exception as e:
            logger.error(f"Error creating thumbnail for {filename}: {e}")
            return None

    async def delete_file(self, file_url: str) -> bool:
        """Удаляет файл с диска"""
        try:
            # Извлекаем путь к файлу из URL
            if file_url.startswith("/uploads/"):
                file_path = self.upload_dir / file_url[9:]  # Убираем '/uploads/'

                if file_path.exists():
                    file_path.unlink()

                    # Удаляем миниатюру если есть
                    if "images/" in str(file_path):
                        thumbnail_path = (
                            self.upload_dir / "thumbnails" / f"thumb_{file_path.name}"
                        )
                        if thumbnail_path.exists():
                            thumbnail_path.unlink()

                    return True
            return False

        except Exception as e:
            logger.error(f"Error deleting file {file_url}: {e}")
            return False

    async def get_file_info(self, file_url: str) -> Optional[Dict]:
        """Получает информацию о файле"""
        try:
            if file_url.startswith("/uploads/"):
                file_path = self.upload_dir / file_url[9:]

                if file_path.exists():
                    stat = file_path.stat()
                    return {
                        "size": stat.st_size,
                        "created": stat.st_ctime,
                        "modified": stat.st_mtime,
                        "exists": True,
                    }
            return None

        except Exception as e:
            logger.error(f"Error getting file info for {file_url}: {e}")
            return None


# Глобальный экземпляр сервиса
media_service = MediaService()
