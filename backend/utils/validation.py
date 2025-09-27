"""
Утилиты для валидации данных
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ValidationError
from fastapi import HTTPException, status
import re


class ValidationUtils:
    """Утилиты для валидации"""

    @staticmethod
    def validate_email(email: str) -> bool:
        """Валидация email адреса"""
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))

    @staticmethod
    def validate_password_strength(password: str) -> Dict[str, Any]:
        """Валидация силы пароля"""
        result = {"is_valid": True, "score": 0, "feedback": []}

        if len(password) < 8:
            result["is_valid"] = False
            result["feedback"].append("Пароль должен содержать минимум 8 символов")
        else:
            result["score"] += 1

        if not re.search(r"[a-z]", password):
            result["feedback"].append("Добавьте строчные буквы")
        else:
            result["score"] += 1

        if not re.search(r"[A-Z]", password):
            result["feedback"].append("Добавьте заглавные буквы")
        else:
            result["score"] += 1

        if not re.search(r"\d", password):
            result["feedback"].append("Добавьте цифры")
        else:
            result["score"] += 1

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            result["feedback"].append("Добавьте специальные символы")
        else:
            result["score"] += 1

        if result["score"] < 3:
            result["is_valid"] = False

        return result

    @staticmethod
    def validate_username(username: str) -> bool:
        """Валидация имени пользователя"""
        pattern = r"^[a-zA-Z0-9_]{3,20}$"
        return bool(re.match(pattern, username))

    @staticmethod
    def validate_slug(slug: str) -> bool:
        """Валидация URL slug"""
        pattern = r"^[a-z0-9-]+$"
        return bool(re.match(pattern, slug))

    @staticmethod
    def sanitize_html(html_content: str) -> str:
        """Очистка HTML контента от потенциально опасных тегов"""
        # Разрешенные теги
        allowed_tags = {
            "p",
            "br",
            "strong",
            "em",
            "u",
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "ul",
            "ol",
            "li",
            "a",
            "img",
            "blockquote",
            "code",
            "pre",
        }

        # Простая очистка - в реальном проекте используйте библиотеку типа bleach
        import re

        # Удаляем все теги кроме разрешенных
        pattern = r"<(?!\/?(?:" + "|".join(allowed_tags) + r")\b)[^>]*>"
        return re.sub(pattern, "", html_content)

    @staticmethod
    def validate_file_upload(
        filename: str, file_size: int, allowed_extensions: List[str], max_size: int
    ) -> Dict[str, Any]:
        """Валидация загружаемого файла"""
        result = {"is_valid": True, "errors": []}

        # Проверка расширения файла
        file_extension = filename.split(".")[-1].lower() if "." in filename else ""
        if file_extension not in allowed_extensions:
            result["is_valid"] = False
            result["errors"].append(
                f"Недопустимое расширение файла. Разрешены: {', '.join(allowed_extensions)}"
            )

        # Проверка размера файла
        if file_size > max_size:
            result["is_valid"] = False
            result["errors"].append(
                f"Файл слишком большой. Максимальный размер: {max_size} байт"
            )

        return result


class PaginationValidator:
    """Валидатор для пагинации"""

    @staticmethod
    def validate_pagination_params(skip: int, limit: int) -> Dict[str, Any]:
        """Валидация параметров пагинации"""
        errors = []

        if skip < 0:
            errors.append("skip должен быть >= 0")

        if limit < 1:
            errors.append("limit должен быть >= 1")
        elif limit > 100:
            errors.append("limit не должен превышать 100")

        return {
            "is_valid": len(errors) == 0,
            "errors": errors,
            "skip": max(0, skip),
            "limit": min(100, max(1, limit)),
        }


class DataValidator:
    """Валидатор данных"""

    @staticmethod
    def validate_model_data(
        model_class: BaseModel, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Валидация данных модели"""
        try:
            validated_data = model_class(**data)
            return {"is_valid": True, "data": validated_data.dict(), "errors": []}
        except ValidationError as e:
            return {
                "is_valid": False,
                "data": None,
                "errors": [
                    {"field": error["loc"][0], "message": error["msg"]}
                    for error in e.errors()
                ],
            }

    @staticmethod
    def validate_required_fields(
        data: Dict[str, Any], required_fields: List[str]
    ) -> Dict[str, Any]:
        """Валидация обязательных полей"""
        missing_fields = [
            field
            for field in required_fields
            if field not in data or data[field] is None
        ]

        return {
            "is_valid": len(missing_fields) == 0,
            "missing_fields": missing_fields,
            "errors": [f"Поле '{field}' обязательно" for field in missing_fields],
        }


def validate_and_raise(
    data: Any, validator_func, error_message: str = "Ошибка валидации"
):
    """Валидация с выбросом исключения при ошибке"""
    result = validator_func(data)
    if not result.get("is_valid", True):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"message": error_message, "errors": result.get("errors", [])},
        )
    return result
