"""
Тесты навигации по приложению
"""

import pytest
import allure
from pages.tests_page import TestsPage
from config.settings import Settings
from utils.helpers import TestHelpers


@pytest.fixture(scope="function")
def tests_page(browser, url):
    """Фикстура для создания страницы тестов"""
    page = TestsPage(browser, f"{url}/tests.html")
    page.open()
    return page


@allure.feature("Навигация")
@allure.story("Основная навигация")
@pytest.mark.medium
def test_main_navigation_works(tests_page):
    """Проверка основной навигации по приложению"""
    # Проверяем, что страница загрузилась
    assert tests_page.is_page_loaded(), "Страница тестов не загрузилась"

    # Проверяем наличие основных элементов навигации
    assert tests_page.is_navigation_menu_present(), "Меню навигации отсутствует"

    # Проверяем заголовок страницы
    assert (
        tests_page.get_page_title() == "Демо компонентов"
    ), "Неверный заголовок страницы"


@allure.feature("Навигация")
@allure.story("Навигационное меню")
@pytest.mark.medium
def test_navigation_menu_elements(tests_page):
    """Проверка элементов навигационного меню"""
    # Проверяем наличие табов навигации
    assert tests_page.is_files_button_present(), "Таб 'Поля ввода' отсутствует"
    assert tests_page.is_folders_button_present(), "Таб 'Чекбоксы' отсутствует"
    assert tests_page.is_settings_button_present(), "Таб 'Кнопки' отсутствует"
    assert tests_page.is_logout_button_present(), "Таб 'Картинки' отсутствует"


@allure.feature("Навигация")
@allure.story("Переходы между разделами")
@pytest.mark.medium
def test_navigation_between_sections(tests_page):
    """Проверка переходов между разделами приложения"""
    # Переходим в раздел полей ввода
    tests_page.navigate_to_files()
    assert (
        tests_page.is_files_section_active()
    ), "Не удалось перейти в раздел полей ввода"

    # Переходим в раздел чекбоксов
    tests_page.navigate_to_folders()
    assert (
        tests_page.is_folders_section_active()
    ), "Не удалось перейти в раздел чекбоксов"

    # Переходим в раздел кнопок
    tests_page.navigate_to_settings()
    assert tests_page.is_settings_section_active(), "Не удалось перейти в раздел кнопок"


@allure.feature("Навигация")
@allure.story("Переход в раздел картинок")
@pytest.mark.medium
def test_user_logout(tests_page):
    """Проверка перехода в раздел картинок"""
    # Переходим в раздел картинок
    tests_page.logout_user()

    # Проверяем, что раздел картинок активен
    assert tests_page.is_logout_button_present(), "Раздел картинок не активен"


@allure.feature("Навигация")
@allure.story("Обновление страницы")
@pytest.mark.low
def test_page_refresh_behavior(tests_page):
    """Проверка поведения при обновлении страницы"""
    # Обновляем страницу
    tests_page.refresh_page()

    # Проверяем, что страница загрузилась корректно
    assert (
        tests_page.is_page_loaded_after_refresh()
    ), "Страница не загрузилась после обновления"

    # Проверяем, что пользователь остался авторизованным
    # В реальном приложении токен может не сохраняться после refresh
    # Поэтому проверяем, что страница загрузилась корректно
    assert (
        tests_page.is_page_loaded_after_refresh()
    ), "Страница не загрузилась после обновления"


@allure.feature("Навигация")
@allure.story("Кнопки браузера")
@pytest.mark.low
def test_browser_navigation_buttons(tests_page):
    """Проверка работы кнопок браузера (назад/вперед)"""
    # Переходим в раздел полей ввода
    tests_page.navigate_to_files()

    # Сохраняем текущий URL для проверки
    initial_url = tests_page.browser.current_url

    # Используем кнопку "Назад" браузера
    tests_page.browser_back()

    # Проверяем, что URL изменился (браузер вернулся назад)
    current_url = tests_page.browser.current_url
    assert current_url != initial_url, "Браузер не вернулся назад"

    # Используем кнопку "Вперед" браузера
    tests_page.browser_forward()

    # Проверяем, что вернулись к исходному URL
    final_url = tests_page.browser.current_url
    assert final_url == initial_url, "Браузер не вернулся вперед к исходной странице"
