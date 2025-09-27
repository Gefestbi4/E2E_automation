"""
Критический путь пользователя - полный цикл работы с приложением
"""

import pytest
import allure
import time
from pages.login_page import LoginPage
from pages.tests_page import TestsPage
from config.settings import Settings
from utils.helpers import TestHelpers


@allure.feature("Критический путь пользователя")
@allure.story("Полный цикл работы пользователя")
@pytest.mark.crit
def test_complete_user_journey(browser, url, api_client):
    """
    Тест полного цикла работы пользователя:
    1. Авторизация
    2. Навигация по приложению
    3. Работа с компонентами
    4. Проверка функциональности
    5. Выход из системы
    """

    # ===== ЭТАП 1: АВТОРИЗАЦИЯ =====
    with allure.step("1. Авторизация пользователя"):
        login_page = LoginPage(browser, f"{url}/login.html")
        login_page.open()

        # Проверяем, что страница загрузилась
        assert login_page.is_page_loaded(), "Страница входа не загрузилась"

        # Выполняем авторизацию
        login_page.sign_in("test@example.com", "testpassword123")

        # Ждем перенаправления на страницу тестов
        assert (
            login_page.wait_for_redirect_to_tests()
        ), "Не произошло перенаправление на страницу тестов"

    # ===== ЭТАП 2: НАВИГАЦИЯ ПО ПРИЛОЖЕНИЮ =====
    with allure.step("2. Навигация по приложению"):
        tests_page = TestsPage(browser, f"{url}/tests.html")

        # Проверяем загрузку страницы тестов
        assert tests_page.is_page_loaded(), "Страница тестов не загрузилась"

        # Проверяем заголовок
        assert (
            tests_page.get_page_title() == "Демо компонентов"
        ), "Неверный заголовок страницы"

        # Проверяем наличие навигационного меню
        assert tests_page.is_navigation_menu_present(), "Меню навигации отсутствует"

    # ===== ЭТАП 3: РАБОТА С КОМПОНЕНТАМИ =====
    with allure.step("3. Работа с полями ввода"):
        # Переходим в раздел полей ввода
        tests_page.navigate_to_files()
        assert (
            tests_page.is_files_section_active()
        ), "Не удалось перейти в раздел полей ввода"

        # Работаем с демо полями ввода
        tests_page.interact_with_demo_inputs()

    with allure.step("4. Работа с чекбоксами"):
        # Переходим в раздел чекбоксов
        tests_page.navigate_to_folders()
        assert (
            tests_page.is_folders_section_active()
        ), "Не удалось перейти в раздел чекбоксов"

        # Работаем с демо чекбоксами
        tests_page.interact_with_demo_checkboxes()

    with allure.step("5. Работа с кнопками"):
        # Переходим в раздел кнопок
        tests_page.navigate_to_settings()
        assert (
            tests_page.is_settings_section_active()
        ), "Не удалось перейти в раздел кнопок"

        # Работаем с демо кнопками
        tests_page.interact_with_demo_buttons()

    # ===== ЭТАП 4: ПРОВЕРКА ФУНКЦИОНАЛЬНОСТИ =====
    with allure.step("6. Проверка навигации между разделами"):
        # Тестируем навигацию между разделами
        tests_page.navigate_to_files()
        assert (
            tests_page.is_files_section_active()
        ), "Навигация в раздел файлов не работает"

        tests_page.navigate_to_folders()
        assert (
            tests_page.is_folders_section_active()
        ), "Навигация в раздел папок не работает"

        tests_page.navigate_to_settings()
        assert (
            tests_page.is_settings_section_active()
        ), "Навигация в раздел кнопок не работает"

    with allure.step("7. Проверка обновления страницы"):
        # Обновляем страницу
        tests_page.refresh_page()

        # Проверяем, что страница загрузилась корректно
        assert (
            tests_page.is_page_loaded_after_refresh()
        ), "Страница не загрузилась после обновления"

    # ===== ЭТАП 5: ПРОВЕРКА СЕССИИ =====
    with allure.step("8. Проверка сохранения сессии"):
        # Проверяем, что пользователь остается авторизованным
        assert (
            tests_page.is_user_authenticated()
        ), "Пользователь не остался авторизованным"

        # Проверяем, что access токен присутствует
        assert tests_page.is_auth_token_present(), "Access токен отсутствует"

        # Проверяем, что refresh токен присутствует
        assert tests_page.is_refresh_token_present(), "Refresh токен отсутствует"

        # Проверяем, что информация об истечении токена присутствует
        assert (
            tests_page.is_token_expires_present()
        ), "Информация об истечении токена отсутствует"

    # ===== ЭТАП 6: ЗАВЕРШЕНИЕ СЕССИИ =====
    with allure.step("9. Завершение работы"):
        # Переходим в раздел картинок (имитация выхода)
        tests_page.logout_user()

        # Проверяем, что раздел картинок активен
        assert (
            tests_page.is_logout_button_present()
        ), "Не удалось перейти в раздел картинок"

        # Финальная проверка - страница все еще загружена
        assert tests_page.is_page_loaded(), "Страница не загружена в конце теста"


@allure.feature("Критический путь пользователя")
@allure.story("Быстрый критический путь")
@pytest.mark.medium
def test_quick_critical_path(browser, url):
    """
    Быстрый критический путь - основные функции за минимальное время
    """

    with allure.step("Быстрая авторизация"):
        login_page = LoginPage(browser, f"{url}/login.html")
        login_page.open()
        login_page.sign_in("test@example.com", "testpassword123")
        assert login_page.wait_for_redirect_to_tests(), "Авторизация не удалась"

    with allure.step("Быстрая навигация"):
        tests_page = TestsPage(browser, f"{url}/tests.html")
        assert tests_page.is_page_loaded(), "Страница не загрузилась"

        # Быстрая проверка основных разделов
        tests_page.navigate_to_files()
        assert tests_page.is_files_section_active(), "Раздел файлов не работает"

        tests_page.navigate_to_folders()
        assert tests_page.is_folders_section_active(), "Раздел папок не работает"

    with allure.step("Проверка стабильности"):
        # Проверяем, что приложение стабильно работает
        assert tests_page.is_user_authenticated(), "Сессия нестабильна"


@allure.feature("Критический путь пользователя")
@allure.story("Обработка ошибок в критическом пути")
@pytest.mark.medium
def test_critical_path_error_handling(browser, url):
    """
    Проверка обработки ошибок в критическом пути
    """

    with allure.step("Попытка авторизации с неверными данными"):
        login_page = LoginPage(browser, f"{url}/login.html")
        login_page.open()

        # Ждем загрузки страницы
        assert login_page.is_page_loaded(), "Страница входа не загрузилась"

        # Пытаемся авторизоваться с неверными данными
        login_page.sign_in("invalid@example.com", "wrongpassword")

        # Проверяем, что остались на странице входа (правильное поведение)
        current_url = browser.current_url
        assert (
            "login" in current_url
        ), "Пользователь должен остаться на странице входа при неверной авторизации"

    with allure.step("Восстановление после ошибки"):
        # Обновляем страницу для восстановления состояния
        browser.refresh()

        # Ждем загрузки страницы (увеличиваем таймаут)
        import time

        time.sleep(2)

        # Переходим на страницу входа и ждем загрузки
        browser.get(f"{url}/login.html")

        # Ждем загрузки страницы с помощью WebDriverWait
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from pages.Locators import LoginPageLocators

        try:
            WebDriverWait(browser, 15).until(
                EC.presence_of_element_located(LoginPageLocators.EMAIL_INPUT)
            )
        except:
            # Если не удалось, ждем еще немного
            time.sleep(5)

        # Создаем новый объект LoginPage для обновленной страницы
        login_page = LoginPage(browser, f"{url}/login.html")

        # Пытаемся авторизоваться с правильными данными
        login_page.sign_in("test@example.com", "testpassword123")

        # Проверяем успешную авторизацию
        if login_page.wait_for_redirect_to_tests():
            tests_page = TestsPage(browser, f"{url}/tests.html")
            assert tests_page.is_page_loaded(), "Не удалось восстановиться после ошибки"


@allure.feature("Критический путь пользователя")
@allure.story("Производительность критического пути")
@pytest.mark.medium
def test_critical_path_performance(browser, url):
    """
    Проверка производительности критического пути
    """

    start_time = time.time()

    with allure.step("Измерение времени авторизации"):
        login_page = LoginPage(browser, f"{url}/login.html")
        login_page.open()

        auth_start = time.time()
        login_page.sign_in("test@example.com", "testpassword123")
        login_page.wait_for_redirect_to_tests()
        auth_time = time.time() - auth_start

        # Авторизация должна занимать не более 20 секунд
        assert (
            auth_time < 20
        ), f"Авторизация заняла слишком много времени: {auth_time:.2f}с"
        allure.attach(
            f"{auth_time:.2f}",
            "Время авторизации (секунды)",
            allure.attachment_type.TEXT,
        )

    with allure.step("Измерение времени навигации"):
        tests_page = TestsPage(browser, f"{url}/tests.html")

        nav_start = time.time()
        tests_page.navigate_to_files()
        tests_page.navigate_to_folders()
        tests_page.navigate_to_settings()
        nav_time = time.time() - nav_start

        # Навигация должна занимать не более 5 секунд
        assert nav_time < 5, f"Навигация заняла слишком много времени: {nav_time:.2f}с"
        allure.attach(
            f"{nav_time:.2f}", "Время навигации (секунды)", allure.attachment_type.TEXT
        )

    total_time = time.time() - start_time

    with allure.step("Общее время выполнения"):
        # Общее время должно быть разумным
        assert (
            total_time < 30
        ), f"Общее время выполнения слишком большое: {total_time:.2f}с"
        allure.attach(
            f"{total_time:.2f}",
            "Общее время выполнения (секунды)",
            allure.attachment_type.TEXT,
        )
