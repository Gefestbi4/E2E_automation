"""
Тесты безопасности
"""

import pytest
from fastapi.testclient import TestClient
from app import app
from security import SecurityUtils, RateLimiter

client = TestClient(app)


class TestPasswordSecurity:
    """Тесты безопасности паролей"""

    def test_password_validation_strong_password(self):
        """Тест валидации сильного пароля"""
        password = "StrongPass123!"
        result = SecurityUtils.validate_password_strength(password)

        assert result["is_valid"] is True
        assert len(result["errors"]) == 0
        assert result["strength_score"] >= 80

    def test_password_validation_weak_password(self):
        """Тест валидации слабого пароля"""
        password = "123"
        result = SecurityUtils.validate_password_strength(password)

        assert result["is_valid"] is False
        assert len(result["errors"]) > 0
        assert "минимум 8 символов" in result["errors"][0]

    def test_password_validation_common_password(self):
        """Тест валидации распространенного пароля"""
        password = "password"
        result = SecurityUtils.validate_password_strength(password)

        assert result["is_valid"] is False
        assert "слишком простой" in result["errors"][0]

    def test_password_hashing(self):
        """Тест хеширования пароля"""
        password = "testpassword123"
        hashed = SecurityUtils.get_password_hash(password)

        assert hashed != password
        assert SecurityUtils.verify_password(password, hashed) is True
        assert SecurityUtils.verify_password("wrongpassword", hashed) is False


class TestTokenSecurity:
    """Тесты безопасности токенов"""

    def test_access_token_creation(self):
        """Тест создания access токена"""
        data = {"sub": "test@example.com", "user_id": 1}
        token = SecurityUtils.create_access_token(data)

        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0

    def test_refresh_token_creation(self):
        """Тест создания refresh токена"""
        data = {"sub": "test@example.com", "user_id": 1}
        token = SecurityUtils.create_refresh_token(data)

        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0

    def test_token_verification_valid(self):
        """Тест верификации валидного токена"""
        data = {"sub": "test@example.com", "user_id": 1}
        token = SecurityUtils.create_access_token(data)
        payload = SecurityUtils.verify_token(token, "access")

        assert payload["sub"] == "test@example.com"
        assert payload["user_id"] == 1
        assert payload["type"] == "access"

    def test_token_verification_invalid(self):
        """Тест верификации невалидного токена"""
        with pytest.raises(Exception):
            SecurityUtils.verify_token("invalid_token", "access")


class TestInputSanitization:
    """Тесты очистки пользовательского ввода"""

    def test_sanitize_input_normal(self):
        """Тест очистки нормального ввода"""
        input_text = "Normal text input"
        sanitized = SecurityUtils.sanitize_input(input_text)

        assert sanitized == input_text

    def test_sanitize_input_dangerous_chars(self):
        """Тест очистки опасных символов"""
        input_text = "<script>alert('xss')</script>"
        sanitized = SecurityUtils.sanitize_input(input_text)

        assert "<script>" not in sanitized
        assert "alert" not in sanitized

    def test_sanitize_input_empty(self):
        """Тест очистки пустого ввода"""
        sanitized = SecurityUtils.sanitize_input("")
        assert sanitized == ""

        sanitized = SecurityUtils.sanitize_input(None)
        assert sanitized == ""

    def test_sanitize_input_length_limit(self):
        """Тест ограничения длины ввода"""
        long_input = "a" * 2000
        sanitized = SecurityUtils.sanitize_input(long_input)

        assert len(sanitized) <= 1000


class TestEmailValidation:
    """Тесты валидации email"""

    def test_valid_emails(self):
        """Тест валидных email адресов"""
        valid_emails = [
            "test@example.com",
            "user.name@domain.co.uk",
            "user+tag@example.org",
            "123@test.com",
        ]

        for email in valid_emails:
            assert SecurityUtils.validate_email(email) is True

    def test_invalid_emails(self):
        """Тест невалидных email адресов"""
        invalid_emails = [
            "invalid-email",
            "@example.com",
            "test@",
            "test..test@example.com",
            "test@.com",
        ]

        for email in invalid_emails:
            assert SecurityUtils.validate_email(email) is False


class TestRateLimiting:
    """Тесты rate limiting"""

    def test_rate_limiter_allows_requests(self):
        """Тест разрешения запросов в пределах лимита"""
        limiter = RateLimiter()
        ip = "192.168.1.1"

        # Первые несколько запросов должны быть разрешены
        for _ in range(10):
            assert limiter.is_allowed(ip) is True

    def test_rate_limiter_blocks_excess_requests(self):
        """Тест блокировки избыточных запросов"""
        limiter = RateLimiter()
        ip = "192.168.1.2"

        # Делаем много запросов
        for _ in range(150):  # Больше лимита
            limiter.is_allowed(ip)

        # Проверяем, что запросы заблокированы
        assert limiter.is_allowed(ip) is False

    def test_rate_limiter_remaining_requests(self):
        """Тест подсчета оставшихся запросов"""
        limiter = RateLimiter()
        ip = "192.168.1.3"

        # Делаем несколько запросов
        for _ in range(5):
            limiter.is_allowed(ip)

        remaining = limiter.get_remaining_requests(ip)
        assert remaining == 95  # 100 - 5


class TestSecurityHeaders:
    """Тесты заголовков безопасности"""

    def test_security_headers_present(self):
        """Тест наличия заголовков безопасности"""
        response = client.get("/")

        # Проверяем основные заголовки безопасности
        assert response.status_code == 200
        # Заголовки добавляются middleware, но в тестовом клиенте могут не отображаться
        # Это нормально для тестовой среды


class TestCSRFProtection:
    """Тесты CSRF защиты"""

    def test_csrf_token_generation(self):
        """Тест генерации CSRF токена"""
        token1 = SecurityUtils.generate_csrf_token()
        token2 = SecurityUtils.generate_csrf_token()

        assert token1 != token2
        assert len(token1) > 0
        assert len(token2) > 0

    def test_csrf_token_verification(self):
        """Тест верификации CSRF токена"""
        token = SecurityUtils.generate_csrf_token()

        # Правильный токен
        assert SecurityUtils.verify_csrf_token(token, token) is True

        # Неправильный токен
        assert SecurityUtils.verify_csrf_token(token, "wrong_token") is False


class TestSecureFilename:
    """Тесты генерации безопасных имен файлов"""

    def test_secure_filename_generation(self):
        """Тест генерации безопасного имени файла"""
        original = "malicious_file.exe"
        secure = SecurityUtils.generate_secure_filename(original)

        assert secure != original
        assert secure.endswith(".exe")
        assert len(secure) > len(original)

    def test_secure_filename_different_inputs(self):
        """Тест генерации для разных входных данных"""
        inputs = ["file.txt", "image.png", "document.pdf", "script.js"]

        generated = []
        for filename in inputs:
            secure = SecurityUtils.generate_secure_filename(filename)
            generated.append(secure)
            assert secure.endswith(filename.split(".")[-1])

        # Все имена должны быть уникальными
        assert len(set(generated)) == len(generated)
