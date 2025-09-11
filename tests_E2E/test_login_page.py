import os
from contextlib import contextmanager
import pytest
from dotenv import load_dotenv
from pages.login_page import LoginPage
from pages.Locators import LeftSidebarLocators
from api.api_user import UserApi

load_dotenv()  # Загружает переменные из .env

api_key = os.getenv('API_KEY')
database_url = os.getenv('DATABASE_URL')
email = os.getenv('EMAIL')
password = os.getenv('PASSWORD')
name = os.getenv('USER_NAME')

@contextmanager
def auth(browser, url):
    """Контекстный менеджер авторизации пользователя"""
    api = UserApi(database_url, api_key)
    api.create_user(email, password, name)
    page = LoginPage(browser, url)
    page.open()
    try:
        yield page
    finally:
        pass

@pytest.mark.crit
def test_sign_in(browser, url):
    """Проверка авторизации пользователя на главной странице Google"""
    with auth(browser, url) as page:
        page.sign_in(email, password)
        main_page_default_url = url
        tab_url = browser.current_url
        assert main_page_default_url == tab_url ,f"Пользователь не авторизовался, текущий URL: {tab_url}"
        assert page.find_element(*LeftSidebarLocators.L_SIDEBAR_BTN_1) ,"Первая кнопка левого меню не найдена"
