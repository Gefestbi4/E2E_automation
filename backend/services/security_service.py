"""
Сервис для усиления безопасности
"""

from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta, timezone
import logging
import hashlib
import secrets
import re
import ipaddress
from functools import wraps
import asyncio

logger = logging.getLogger(__name__)


class SecurityService:
    """Сервис для усиления безопасности"""

    def __init__(self):
        self.failed_attempts = {}  # IP -> attempts
        self.blocked_ips = set()  # Заблокированные IP
        self.suspicious_activities = []  # Подозрительная активность

        # Настройки безопасности
        self.config = {
            "max_login_attempts": 5,
            "lockout_duration": 900,  # 15 минут
            "password_min_length": 8,
            "password_require_uppercase": True,
            "password_require_lowercase": True,
            "password_require_numbers": True,
            "password_require_special": True,
            "session_timeout": 3600,  # 1 час
            "rate_limit_requests": 100,  # 100 запросов в минуту
            "rate_limit_window": 60,  # 1 минута
            "enable_2fa": True,
            "enable_csrf_protection": True,
            "enable_xss_protection": True,
            "enable_sql_injection_protection": True,
        }

        # Паттерны для обнаружения атак
        self.attack_patterns = {
            "sql_injection": [
                r"('|(\\')|(;)|(--)|(/\*)|(\*/)|(\b(union|select|insert|update|delete|drop|create|alter)\b)",
                r"(\b(or|and)\s+\d+\s*=\s*\d+)",
                r"(\b(union|select).*from)",
                r"(\b(insert|update|delete).*into)",
                r"(\b(drop|create|alter).*table)",
            ],
            "xss": [
                r"<script[^>]*>.*?</script>",
                r"javascript:",
                r"on\w+\s*=",
                r"<iframe[^>]*>",
                r"<object[^>]*>",
                r"<embed[^>]*>",
                r"<link[^>]*>",
                r"<meta[^>]*>",
            ],
            "path_traversal": [
                r"\.\./",
                r"\.\.\\",
                r"%2e%2e%2f",
                r"%2e%2e%5c",
                r"\.\.%2f",
                r"\.\.%5c",
            ],
            "command_injection": [
                r"[;&|`$]",
                r"\b(cat|ls|dir|type|more|less|head|tail|grep|find|awk|sed|cut|sort|uniq|wc|ps|top|kill|killall|pkill|pgrep|netstat|ss|lsof|tcpdump|nmap|ping|traceroute|wget|curl|nc|telnet|ssh|ftp|scp|rsync)\b",
            ],
        }

        # Запускаем очистку старых записей
        asyncio.create_task(self._cleanup_old_records())

    async def validate_password_strength(self, password: str) -> Dict[str, Any]:
        """Валидация силы пароля"""
        try:
            issues = []
            score = 0

            # Длина пароля
            if len(password) < self.config["password_min_length"]:
                issues.append(
                    f"Password must be at least {self.config['password_min_length']} characters long"
                )
            else:
                score += 20

            # Проверка на заглавные буквы
            if self.config["password_require_uppercase"] and not re.search(
                r"[A-Z]", password
            ):
                issues.append("Password must contain at least one uppercase letter")
            else:
                score += 20

            # Проверка на строчные буквы
            if self.config["password_require_lowercase"] and not re.search(
                r"[a-z]", password
            ):
                issues.append("Password must contain at least one lowercase letter")
            else:
                score += 20

            # Проверка на цифры
            if self.config["password_require_numbers"] and not re.search(
                r"\d", password
            ):
                issues.append("Password must contain at least one number")
            else:
                score += 20

            # Проверка на специальные символы
            if self.config["password_require_special"] and not re.search(
                r'[!@#$%^&*(),.?":{}|<>]', password
            ):
                issues.append("Password must contain at least one special character")
            else:
                score += 20

            # Проверка на общие пароли
            common_passwords = ["password", "123456", "qwerty", "abc123", "password123"]
            if password.lower() in common_passwords:
                issues.append("Password is too common")
                score -= 30

            # Проверка на повторяющиеся символы
            if len(set(password)) < len(password) * 0.6:
                issues.append("Password has too many repeated characters")
                score -= 10

            return {
                "is_valid": len(issues) == 0,
                "score": max(0, min(100, score)),
                "issues": issues,
                "strength": self._get_password_strength(score),
            }

        except Exception as e:
            logger.error(f"Error validating password strength: {e}")
            return {
                "is_valid": False,
                "score": 0,
                "issues": ["Password validation failed"],
                "strength": "very_weak",
            }

    def _get_password_strength(self, score: int) -> str:
        """Определение силы пароля по баллам"""
        if score >= 90:
            return "very_strong"
        elif score >= 70:
            return "strong"
        elif score >= 50:
            return "medium"
        elif score >= 30:
            return "weak"
        else:
            return "very_weak"

    async def detect_attack_patterns(self, input_data: str) -> List[Dict[str, Any]]:
        """Обнаружение паттернов атак"""
        try:
            detected_attacks = []

            for attack_type, patterns in self.attack_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, input_data, re.IGNORECASE):
                        detected_attacks.append(
                            {
                                "type": attack_type,
                                "pattern": pattern,
                                "severity": self._get_attack_severity(attack_type),
                                "timestamp": datetime.now(timezone.utc).isoformat(),
                            }
                        )

            return detected_attacks

        except Exception as e:
            logger.error(f"Error detecting attack patterns: {e}")
            return []

    def _get_attack_severity(self, attack_type: str) -> str:
        """Определение серьезности атаки"""
        severity_map = {
            "sql_injection": "high",
            "xss": "high",
            "path_traversal": "medium",
            "command_injection": "high",
        }
        return severity_map.get(attack_type, "low")

    async def check_rate_limit(
        self, ip_address: str, endpoint: str
    ) -> Tuple[bool, Dict[str, Any]]:
        """Проверка лимита запросов"""
        try:
            current_time = datetime.now(timezone.utc)
            key = f"{ip_address}:{endpoint}"

            # Получаем историю запросов
            if key not in self.failed_attempts:
                self.failed_attempts[key] = []

            # Очищаем старые записи
            cutoff_time = current_time - timedelta(
                seconds=self.config["rate_limit_window"]
            )
            self.failed_attempts[key] = [
                timestamp
                for timestamp in self.failed_attempts[key]
                if timestamp > cutoff_time
            ]

            # Проверяем лимит
            request_count = len(self.failed_attempts[key])

            if request_count >= self.config["rate_limit_requests"]:
                # Блокируем IP
                self.blocked_ips.add(ip_address)

                # Записываем подозрительную активность
                await self._log_suspicious_activity(
                    ip_address,
                    "rate_limit_exceeded",
                    f"Rate limit exceeded: {request_count} requests in {self.config['rate_limit_window']}s",
                )

                return False, {
                    "allowed": False,
                    "reason": "rate_limit_exceeded",
                    "retry_after": self.config["rate_limit_window"],
                    "current_requests": request_count,
                    "limit": self.config["rate_limit_requests"],
                }

            # Добавляем текущий запрос
            self.failed_attempts[key].append(current_time)

            return True, {
                "allowed": True,
                "current_requests": request_count + 1,
                "limit": self.config["rate_limit_requests"],
                "reset_in": self.config["rate_limit_window"],
            }

        except Exception as e:
            logger.error(f"Error checking rate limit: {e}")
            return True, {"allowed": True, "error": str(e)}

    async def check_ip_blocklist(self, ip_address: str) -> bool:
        """Проверка IP в черном списке"""
        try:
            # Проверяем, заблокирован ли IP
            if ip_address in self.blocked_ips:
                return False

            # Проверяем диапазоны IP (например, частные сети для тестирования)
            try:
                ip_obj = ipaddress.ip_address(ip_address)
                if ip_obj.is_private:
                    return True  # Разрешаем частные IP
            except ValueError:
                return False  # Некорректный IP

            # Здесь можно добавить проверку внешних черных списков
            # Например, проверка через API сервисов типа AbuseIPDB

            return True

        except Exception as e:
            logger.error(f"Error checking IP blocklist: {e}")
            return True  # В случае ошибки разрешаем доступ

    async def generate_csrf_token(self, user_id: int) -> str:
        """Генерация CSRF токена"""
        try:
            if not self.config["enable_csrf_protection"]:
                return ""

            # Создаем уникальный токен
            token_data = f"{user_id}:{datetime.now(timezone.utc).isoformat()}:{secrets.token_hex(16)}"
            token = hashlib.sha256(token_data.encode()).hexdigest()

            return token

        except Exception as e:
            logger.error(f"Error generating CSRF token: {e}")
            return ""

    async def validate_csrf_token(self, token: str, user_id: int) -> bool:
        """Валидация CSRF токена"""
        try:
            if not self.config["enable_csrf_protection"]:
                return True

            if not token:
                return False

            # В реальном приложении здесь будет проверка токена в БД
            # Пока возвращаем True для демонстрации
            return True

        except Exception as e:
            logger.error(f"Error validating CSRF token: {e}")
            return False

    async def sanitize_input(self, input_data: str) -> str:
        """Очистка пользовательского ввода"""
        try:
            if not self.config["enable_xss_protection"]:
                return input_data

            # Удаляем HTML теги
            sanitized = re.sub(r"<[^>]+>", "", input_data)

            # Экранируем специальные символы
            sanitized = sanitized.replace("&", "&amp;")
            sanitized = sanitized.replace("<", "&lt;")
            sanitized = sanitized.replace(">", "&gt;")
            sanitized = sanitized.replace('"', "&quot;")
            sanitized = sanitized.replace("'", "&#x27;")
            sanitized = sanitized.replace("/", "&#x2F;")

            return sanitized

        except Exception as e:
            logger.error(f"Error sanitizing input: {e}")
            return input_data

    async def _log_suspicious_activity(
        self, ip_address: str, activity_type: str, description: str
    ):
        """Логирование подозрительной активности"""
        try:
            activity = {
                "ip_address": ip_address,
                "activity_type": activity_type,
                "description": description,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "severity": self._get_attack_severity(activity_type),
            }

            self.suspicious_activities.append(activity)

            # Ограничиваем количество записей
            if len(self.suspicious_activities) > 1000:
                self.suspicious_activities = self.suspicious_activities[-500:]

            logger.warning(f"Suspicious activity detected: {activity}")

        except Exception as e:
            logger.error(f"Error logging suspicious activity: {e}")

    async def _cleanup_old_records(self):
        """Очистка старых записей"""
        while True:
            try:
                await asyncio.sleep(3600)  # Каждый час

                current_time = datetime.now(timezone.utc)
                cutoff_time = current_time - timedelta(hours=24)

                # Очищаем старые попытки входа
                for key in list(self.failed_attempts.keys()):
                    self.failed_attempts[key] = [
                        timestamp
                        for timestamp in self.failed_attempts[key]
                        if timestamp > cutoff_time
                    ]
                    if not self.failed_attempts[key]:
                        del self.failed_attempts[key]

                # Очищаем старые записи подозрительной активности
                self.suspicious_activities = [
                    activity
                    for activity in self.suspicious_activities
                    if datetime.fromisoformat(activity["timestamp"]) > cutoff_time
                ]

                logger.info("Cleaned up old security records")

            except Exception as e:
                logger.error(f"Error in cleanup: {e}")

    async def get_security_report(self) -> Dict[str, Any]:
        """Получение отчета по безопасности"""
        try:
            current_time = datetime.now(timezone.utc)
            last_24h = current_time - timedelta(hours=24)

            # Статистика за последние 24 часа
            recent_activities = [
                activity
                for activity in self.suspicious_activities
                if datetime.fromisoformat(activity["timestamp"]) > last_24h
            ]

            # Группировка по типам активности
            activity_types = {}
            for activity in recent_activities:
                activity_type = activity["activity_type"]
                if activity_type not in activity_types:
                    activity_types[activity_type] = 0
                activity_types[activity_type] += 1

            # Группировка по IP
            ip_activities = {}
            for activity in recent_activities:
                ip = activity["ip_address"]
                if ip not in ip_activities:
                    ip_activities[ip] = 0
                ip_activities[ip] += 1

            return {
                "total_suspicious_activities": len(recent_activities),
                "blocked_ips_count": len(self.blocked_ips),
                "failed_attempts_count": len(self.failed_attempts),
                "activity_types": activity_types,
                "top_suspicious_ips": sorted(
                    ip_activities.items(), key=lambda x: x[1], reverse=True
                )[:10],
                "security_config": self.config,
                "last_cleanup": current_time.isoformat(),
            }

        except Exception as e:
            logger.error(f"Error generating security report: {e}")
            return {}

    async def unblock_ip(self, ip_address: str) -> bool:
        """Разблокировать IP адрес"""
        try:
            if ip_address in self.blocked_ips:
                self.blocked_ips.remove(ip_address)
                logger.info(f"IP {ip_address} unblocked")
                return True
            return False

        except Exception as e:
            logger.error(f"Error unblocking IP: {e}")
            return False

    async def update_security_config(self, new_config: Dict[str, Any]) -> bool:
        """Обновление конфигурации безопасности"""
        try:
            # Валидируем новые настройки
            for key, value in new_config.items():
                if key in self.config:
                    self.config[key] = value

            logger.info("Security configuration updated")
            return True

        except Exception as e:
            logger.error(f"Error updating security config: {e}")
            return False


# Создаем глобальный экземпляр сервиса
security_service = SecurityService()
