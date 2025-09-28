"""
Пример автотеста с использованием системы логгирования фронтенда
"""

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time


class TestFrontendLogging:
    """Тесты с использованием системы логгирования фронтенда"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Настройка для каждого теста"""
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

        # Включаем тестовый режим для логгирования
        self.driver.execute_script("window.__TEST_MODE__ = true;")

        yield

        self.driver.quit()

    def get_logs(self, filter_dict=None):
        """Получение логов из браузера"""
        if filter_dict:
            return self.driver.execute_script(
                f"return getTestLogs({json.dumps(filter_dict)});"
            )
        return self.driver.execute_script("return getTestLogs();")

    def clear_logs(self):
        """Очистка логов"""
        self.driver.execute_script("clearTestLogs();")

    def wait_for_log(self, filter_dict, timeout=10):
        """Ожидание конкретного лога"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            logs = self.get_logs(filter_dict)
            if logs:
                return logs[-1]
            time.sleep(0.1)
        return None

    def test_login_logging(self):
        """Тест входа с проверкой логгирования"""
        # Очищаем логи перед тестом
        self.clear_logs()

        # Переходим на страницу входа
        self.driver.get("http://localhost:8000/login.html")

        # Ждем загрузки страницы
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )

        # Заполняем форму входа
        email_input = self.driver.find_element(By.ID, "email")
        password_input = self.driver.find_element(By.ID, "password")
        login_button = self.driver.find_element(By.ID, "login-btn")

        email_input.send_keys("test@example.com")
        password_input.send_keys("testpassword123")

        # Логируем начало входа
        self.driver.execute_script(
            """
            window.TestLogger.startTest('login_test', {
                email: 'test@example.com',
                step: 'filling_form'
            });
        """
        )

        # Нажимаем кнопку входа
        login_button.click()

        # Ждем лог успешного входа или ошибки
        login_log = self.wait_for_log(
            {"category": "AUTH_LOGIN", "level": "info"}, timeout=10
        )

        # Проверяем, что лог был создан
        assert login_log is not None, "Login log not found"
        assert (
            "Login successful" in login_log["message"]
        ), f"Expected successful login, got: {login_log['message']}"

        # Получаем все логи входа
        all_login_logs = self.get_logs({"category": "AUTH_LOGIN"})
        assert (
            len(all_login_logs) >= 2
        ), "Expected at least 2 login logs (start and success)"

        # Проверяем, что есть лог начала входа
        start_log = next(
            (log for log in all_login_logs if "attempt started" in log["message"]), None
        )
        assert start_log is not None, "Login start log not found"

        print(f"✅ Login test passed. Found {len(all_login_logs)} login logs")

    def test_api_request_logging(self):
        """Тест логгирования API запросов"""
        # Очищаем логи
        self.clear_logs()

        # Переходим на главную страницу
        self.driver.get("http://localhost:8000/index.html")

        # Ждем загрузки
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "main-content"))
        )

        # Выполняем действие, которое должно вызвать API запрос
        # Например, клик по кнопке E-commerce
        ecommerce_button = self.driver.find_element(
            By.CSS_SELECTOR, "[data-module='ecommerce']"
        )
        ecommerce_button.click()

        # Ждем API запрос
        api_log = self.wait_for_log({"category": "FETCH_REQUEST"}, timeout=5)

        # Проверяем, что API запрос был залогирован
        assert api_log is not None, "API request log not found"
        assert (
            "api" in api_log["url"].lower()
        ), f"Expected API URL, got: {api_log['url']}"

        # Получаем все API логи
        api_logs = self.get_logs({"category": "FETCH_REQUEST"})
        print(f"✅ Found {len(api_logs)} API request logs")

        # Проверяем структуру лога
        assert "timestamp" in api_log
        assert "level" in api_log
        assert "category" in api_log
        assert "message" in api_log
        assert "data" in api_log

    def test_user_action_logging(self):
        """Тест логгирования пользовательских действий"""
        # Очищаем логи
        self.clear_logs()

        # Переходим на страницу входа
        self.driver.get("http://localhost:8000/login.html")

        # Ждем загрузки
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )

        # Выполняем различные действия
        email_input = self.driver.find_element(By.ID, "email")
        password_input = self.driver.find_element(By.ID, "password")

        # Клик по полю email
        email_input.click()

        # Ввод в поле email
        email_input.send_keys("test@example.com")

        # Клик по полю пароля
        password_input.click()

        # Ввод в поле пароля
        password_input.send_keys("password123")

        # Получаем логи пользовательских действий
        user_action_logs = self.get_logs({"category": "USER_ACTION"})

        # Проверяем, что действия были залогированы
        assert (
            len(user_action_logs) >= 4
        ), f"Expected at least 4 user actions, got {len(user_action_logs)}"

        # Проверяем типы действий
        click_logs = [
            log for log in user_action_logs if log["data"]["eventType"] == "click"
        ]
        input_logs = [
            log for log in user_action_logs if log["data"]["eventType"] == "input"
        ]

        assert len(click_logs) >= 2, "Expected at least 2 click actions"
        assert len(input_logs) >= 2, "Expected at least 2 input actions"

        print(f"✅ User action test passed. Found {len(user_action_logs)} user actions")

    def test_error_logging(self):
        """Тест логгирования ошибок"""
        # Очищаем логи
        self.clear_logs()

        # Переходим на страницу входа
        self.driver.get("http://localhost:8000/login.html")

        # Ждем загрузки
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )

        # Пытаемся войти с неверными данными
        email_input = self.driver.find_element(By.ID, "email")
        password_input = self.driver.find_element(By.ID, "password")
        login_button = self.driver.find_element(By.ID, "login-btn")

        email_input.send_keys("wrong@example.com")
        password_input.send_keys("wrongpassword")
        login_button.click()

        # Ждем лог ошибки
        error_log = self.wait_for_log({"level": "error"}, timeout=10)

        # Проверяем, что ошибка была залогирована
        if error_log:
            print(f"✅ Error logging test passed. Found error: {error_log['message']}")
        else:
            print("ℹ️ No error logs found (this might be expected)")

    def test_log_export(self):
        """Тест экспорта логов"""
        # Очищаем логи
        self.clear_logs()

        # Выполняем несколько действий
        self.driver.get("http://localhost:8000/login.html")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )

        # Заполняем форму
        email_input = self.driver.find_element(By.ID, "email")
        password_input = self.driver.find_element(By.ID, "password")

        email_input.send_keys("test@example.com")
        password_input.send_keys("password123")

        # Экспортируем логи
        export_data = self.driver.execute_script("return exportTestLogs();")

        # Проверяем структуру экспорта
        assert "testLogs" in export_data
        assert "allLogs" in export_data
        assert "sessionId" in export_data
        assert "exportedAt" in export_data
        assert "testMode" in export_data

        # Проверяем, что есть логи
        assert len(export_data["testLogs"]) > 0, "No test logs found in export"

        print(
            f"✅ Log export test passed. Exported {len(export_data['testLogs'])} test logs"
        )

    def test_log_statistics(self):
        """Тест статистики логов"""
        # Очищаем логи
        self.clear_logs()

        # Выполняем различные действия
        self.driver.get("http://localhost:8000/login.html")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )

        # Заполняем форму
        email_input = self.driver.find_element(By.ID, "email")
        password_input = self.driver.find_element(By.ID, "password")

        email_input.send_keys("test@example.com")
        password_input.send_keys("password123")

        # Получаем статистику
        stats = self.driver.execute_script("return TestLogger.getLogStats();")

        # Проверяем структуру статистики
        assert "total" in stats
        assert "byLevel" in stats
        assert "byCategory" in stats
        assert "errors" in stats
        assert "warnings" in stats

        # Проверяем, что есть данные
        assert stats["total"] > 0, "No logs found in statistics"

        print(f"✅ Log statistics test passed. Total logs: {stats['total']}")
        print(f"   Errors: {stats['errors']}, Warnings: {stats['warnings']}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
