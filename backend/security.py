"""
Модуль безопасности для приложения
"""

import secrets
import hashlib
import hmac
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from fastapi import HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from config import settings
import logging

logger = logging.getLogger(__name__)

# Настройки безопасности
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Контекст для хеширования паролей
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# HTTP Bearer для аутентификации
security = HTTPBearer()

# Настройки rate limiting
RATE_LIMIT_REQUESTS = 100  # Максимум запросов
RATE_LIMIT_WINDOW = 3600  # Окно в секундах (1 час)

# Настройки безопасности паролей
MIN_PASSWORD_LENGTH = 8
REQUIRE_UPPERCASE = True
REQUIRE_LOWERCASE = True
REQUIRE_NUMBERS = True
REQUIRE_SPECIAL_CHARS = True

# Список запрещенных паролей
COMMON_PASSWORDS = {
    "password",
    "123456",
    "123456789",
    "qwerty",
    "abc123",
    "password123",
    "admin",
    "letmein",
    "welcome",
    "monkey",
    "dragon",
    "master",
    "hello",
    "login",
    "princess",
}


class SecurityUtils:
    """Утилиты для работы с безопасностью"""

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Проверка пароля"""
        # Ограничиваем длину пароля для bcrypt (72 байта)
        if len(plain_password) > 72:
            plain_password = plain_password[:72]
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Хеширование пароля"""
        # Ограничиваем длину пароля для bcrypt (72 байта)
        if len(password) > 72:
            password = password[:72]
        return pwd_context.hash(password)

    @staticmethod
    def validate_password_strength(password: str) -> Dict[str, Any]:
        """Проверка силы пароля"""
        errors = []
        warnings = []

        if password.lower() in COMMON_PASSWORDS:
            errors.append("Пароль слишком простой")

        if len(password) < MIN_PASSWORD_LENGTH:
            errors.append(
                f"Пароль должен содержать минимум {MIN_PASSWORD_LENGTH} символов"
            )

        if REQUIRE_UPPERCASE and not any(c.isupper() for c in password):
            errors.append("Пароль должен содержать заглавные буквы")

        if REQUIRE_LOWERCASE and not any(c.islower() for c in password):
            errors.append("Пароль должен содержать строчные буквы")

        if REQUIRE_NUMBERS and not any(c.isdigit() for c in password):
            errors.append("Пароль должен содержать цифры")

        if REQUIRE_SPECIAL_CHARS and not any(
            c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password
        ):
            errors.append("Пароль должен содержать специальные символы")

        # Проверка на повторяющиеся символы
        if len(set(password)) < len(password) * 0.6:
            warnings.append("Пароль содержит много повторяющихся символов")

        return {
            "is_valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "strength_score": SecurityUtils._calculate_password_strength(password),
        }

    @staticmethod
    def _calculate_password_strength(password: str) -> int:
        """Расчет силы пароля (0-100)"""
        score = 0

        # Длина пароля
        if len(password) >= 8:
            score += 20
        if len(password) >= 12:
            score += 10
        if len(password) >= 16:
            score += 10

        # Разнообразие символов
        if any(c.isupper() for c in password):
            score += 10
        if any(c.islower() for c in password):
            score += 10
        if any(c.isdigit() for c in password):
            score += 10
        if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            score += 15

        # Уникальность символов
        unique_chars = len(set(password))
        if unique_chars >= len(password) * 0.8:
            score += 15

        return min(score, 100)

    @staticmethod
    def create_access_token(
        data: dict, expires_delta: Optional[timedelta] = None
    ) -> str:
        """Создание JWT access токена"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(
                minutes=ACCESS_TOKEN_EXPIRE_MINUTES
            )

        to_encode.update(
            {
                "exp": expire,
                "type": "access",
                "iat": datetime.now(timezone.utc),
                "jti": secrets.token_urlsafe(32),  # JWT ID для отзыва токенов
            }
        )

        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def create_refresh_token(data: dict) -> str:
        """Создание JWT refresh токена"""
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

        to_encode.update(
            {
                "exp": expire,
                "type": "refresh",
                "iat": datetime.now(timezone.utc),
                "jti": secrets.token_urlsafe(32),
            }
        )

        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def verify_token(token: str, token_type: str = "access") -> Dict[str, Any]:
        """Проверка JWT токена"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

            # Проверка типа токена
            if payload.get("type") != token_type:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Неверный тип токена",
                )

            # Проверка срока действия
            exp = payload.get("exp")
            if exp and datetime.fromtimestamp(exp, tz=timezone.utc) < datetime.now(
                timezone.utc
            ):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен истек"
                )

            return payload

        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный токен"
            )

    @staticmethod
    def generate_csrf_token() -> str:
        """Генерация CSRF токена"""
        return secrets.token_urlsafe(32)

    @staticmethod
    def verify_csrf_token(token: str, session_token: str) -> bool:
        """Проверка CSRF токена"""
        return hmac.compare_digest(token, session_token)

    @staticmethod
    def sanitize_input(text: str) -> str:
        """Очистка пользовательского ввода"""
        if not text:
            return ""

        # Удаление потенциально опасных символов и тегов
        dangerous_chars = ["<", ">", '"', "'", "&", "\x00", "\r", "\n"]
        for char in dangerous_chars:
            text = text.replace(char, "")

        # Удаление JavaScript-подобных конструкций
        import re

        text = re.sub(r"script", "", text, flags=re.IGNORECASE)
        text = re.sub(r"javascript:", "", text, flags=re.IGNORECASE)
        text = re.sub(r"alert\s*\(", "", text, flags=re.IGNORECASE)

        # Ограничение длины
        return text[:1000]

    @staticmethod
    def validate_email(email: str) -> bool:
        """Валидация email адреса"""
        import re

        # Строгая валидация email
        pattern = r"^[a-zA-Z0-9]([a-zA-Z0-9._+-]*[a-zA-Z0-9])?@[a-zA-Z0-9]([a-zA-Z0-9.-]*[a-zA-Z0-9])?\.[a-zA-Z]{2,}$"

        # Дополнительные проверки
        if not re.match(pattern, email):
            return False

        # Проверка на двойные точки
        if ".." in email:
            return False

        # Проверка на точки в начале или конце локальной части
        local, domain = email.split("@", 1)
        if local.startswith(".") or local.endswith("."):
            return False

        return True

    @staticmethod
    def generate_secure_filename(original_filename: str) -> str:
        """Генерация безопасного имени файла"""
        import os
        import uuid

        # Получаем расширение файла
        _, ext = os.path.splitext(original_filename)

        # Генерируем уникальное имя
        secure_name = f"{uuid.uuid4().hex}{ext}"

        return secure_name


class RateLimiter:
    """Rate limiter для ограничения количества запросов"""

    def __init__(self):
        self.requests = {}  # {ip: [(timestamp, count)]}

    def is_allowed(self, ip: str) -> bool:
        """Проверка, разрешен ли запрос"""
        now = datetime.now(timezone.utc)
        window_start = now - timedelta(seconds=RATE_LIMIT_WINDOW)

        # Очистка старых записей
        if ip in self.requests:
            self.requests[ip] = [
                (timestamp, count)
                for timestamp, count in self.requests[ip]
                if timestamp > window_start
            ]
        else:
            self.requests[ip] = []

        # Подсчет запросов в окне
        current_requests = len(self.requests[ip])

        if current_requests >= RATE_LIMIT_REQUESTS:
            return False

        # Добавление текущего запроса
        self.requests[ip].append((now, 1))
        return True

    def get_remaining_requests(self, ip: str) -> int:
        """Получение количества оставшихся запросов"""
        now = datetime.now(timezone.utc)
        window_start = now - timedelta(seconds=RATE_LIMIT_WINDOW)

        if ip not in self.requests:
            return RATE_LIMIT_REQUESTS

        # Очистка старых записей
        self.requests[ip] = [
            (timestamp, count)
            for timestamp, count in self.requests[ip]
            if timestamp > window_start
        ]

        current_requests = len(self.requests[ip])
        return max(0, RATE_LIMIT_REQUESTS - current_requests)


# Глобальный экземпляр rate limiter
rate_limiter = RateLimiter()


def get_client_ip(request: Request) -> str:
    """Получение IP адреса клиента"""
    # Проверяем заголовки прокси
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()

    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip

    # Возвращаем IP клиента
    return request.client.host if request.client else "unknown"


def check_rate_limit(request: Request) -> bool:
    """Проверка rate limit"""
    ip = get_client_ip(request)
    return rate_limiter.is_allowed(ip)


def get_remaining_requests(request: Request) -> int:
    """Получение количества оставшихся запросов"""
    ip = get_client_ip(request)
    return rate_limiter.get_remaining_requests(ip)


# Создаем экземпляр для удобства использования
security_utils = SecurityUtils()


# Экспортируем основные функции
def get_password_hash(password: str) -> str:
    """Хеширование пароля"""
    return security_utils.get_password_hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверка пароля"""
    return security_utils.verify_password(plain_password, hashed_password)
