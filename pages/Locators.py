
from selenium.webdriver.common.by import By

# --- Локаторы для отдельных страниц ---

class LoginPageLocators:
    """Локаторы для страницы входа"""
    EMAIL = (By.CSS_SELECTOR, "")
    PASSWORD = (By.CSS_SELECTOR, "")
    SIGN_IN = (By.CSS_SELECTOR, "")
    SIGN_UP = (By.CSS_SELECTOR, "")


# --- Локаторы для переиспользуемых компонентов ---

class LeftSidebarLocators:
    """Локаторы для левой боковой панели"""
    L_SIDEBAR_BTN_1 = (By.CSS_SELECTOR, "")
    L_SIDEBAR_BTN_2 = (By.CSS_SELECTOR, "")
    L_SIDEBAR_BTN_3 = (By.CSS_SELECTOR, "")
    L_SIDEBAR_BTN_4 = (By.CSS_SELECTOR, "")
    L_SIDEBAR_BTN_5 = (By.CSS_SELECTOR, "")
    L_SIDEBAR_BTN_6 = (By.CSS_SELECTOR, "")

class RightSidebarLocators:
    """Локаторы для правой боковой панели"""
    R_SIDEBAR_BTN_1 = (By.CSS_SELECTOR, "")
    R_SIDEBAR_BTN_2 = (By.CSS_SELECTOR, "")
    R_SIDEBAR_BTN_3 = (By.CSS_SELECTOR, "")
    R_SIDEBAR_BTN_4 = (By.CSS_SELECTOR, "")
    R_SIDEBAR_BTN_5 = (By.CSS_SELECTOR, "")
    R_SIDEBAR_BTN_6 = (By.CSS_SELECTOR, "")
    R_SIDEBAR_BTN_7 = (By.CSS_SELECTOR, "")
    R_SIDEBAR_BTN_8 = (By.CSS_SELECTOR, "")

class NotificationToastLocators:
    """Локаторы для всплывающих уведомлений (тостов)"""
    SUCCESS_TOAST = (By.CSS_SELECTOR, "")
    ERROR_TOAST = (By.CSS_SELECTOR, "")


# --- Локаторы для компонентов главной страницы (вместо MainPageLocators) ---

class SearchComponentLocators:
    """Локаторы для компонента поиска"""
    SEARCH_FIELD = (By.CSS_SELECTOR, "")
    SUBMIT_BTN = (By.CSS_SELECTOR, "")
    CANCEL_BTN = (By.CSS_SELECTOR, "")

class FilterComponentLocators:
    """Локаторы для компонента фильтрации"""
    CHECKBOX1 = (By.CSS_SELECTOR, "")
    CHECKBOX2 = (By.CSS_SELECTOR, "")
    CHECKBOX3 = (By.CSS_SELECTOR, "")
    CHECKBOX_ALL = (By.CSS_SELECTOR, "")
    RADIOBUTTON_1 = (By.CSS_SELECTOR, "")
    RADIOBUTTON_2 = (By.CSS_SELECTOR, "")
    RADIOBUTTON_3 = (By.CSS_SELECTOR, "")
    RADIOBUTTON_4 = (By.CSS_SELECTOR, "")
    FILTER_1 = (By.CSS_SELECTOR, "")
    FILTER_2 = (By.CSS_SELECTOR, "")
    FILTER_3 = (By.CSS_SELECTOR, "")
    FILTER_4 = (By.CSS_SELECTOR, "")

class ResultsGridLocators:
    """Локаторы для сетки с результатами (например, карточки товаров)"""
    THUMBNAIL_1 = (By.CSS_SELECTOR, "")
    THUMBNAIL_2 = (By.CSS_SELECTOR, "")
    THUMBNAIL_3 = (By.CSS_SELECTOR, "")
    THUMBNAIL_4 = (By.CSS_SELECTOR, "")

class FormComponentLocators:
    """Локаторы для другой формы на странице"""
    FIELD_1 = (By.CSS_SELECTOR, "")
    FIELD_2 = (By.CSS_SELECTOR, "")
    FIELD_3 = (By.CSS_SELECTOR, "")

