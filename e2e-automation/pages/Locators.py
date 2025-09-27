from selenium.webdriver.common.by import By


class BaseLocators:
    """Базовые локаторы, общие для всех страниц"""

    # Общие элементы
    HEADER = (By.TAG_NAME, "header")
    MAIN_CONTENT = (By.TAG_NAME, "main")

    # Навигация
    AUTH_LINK = (By.CSS_SELECTOR, "[test-id='auth-link']")
    AUTH_BUTTON = (By.CSS_SELECTOR, "[test-id='auth-button']")

    # Контакты
    EMAIL_LINK = (By.CSS_SELECTOR, "[test-id='email-link']")
    PHONE_LINK = (By.CSS_SELECTOR, "[test-id='phone-link']")
    TELEGRAM_LINK = (By.CSS_SELECTOR, "[test-id='telegram-link']")


class MainPageLocators(BaseLocators):
    """Локаторы главной страницы (index.html)"""

    # Заголовки
    PAGE_TITLE = (By.CSS_SELECTOR, "h1.name")

    # Форма оффера
    OFFER_FORM = (By.CSS_SELECTOR, "[test-id='offer-form']")
    TELEGRAM_INPUT = (By.CSS_SELECTOR, "[test-id='telegram-input']")
    COMMENT_TEXTAREA = (By.CSS_SELECTOR, "[test-id='comment-textarea']")
    SUMMA_SLIDER = (By.CSS_SELECTOR, "[test-id='summa-slider']")
    SUMMA_VALUE = (By.CSS_SELECTOR, "[test-id='summa-value']")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "[test-id='submit-button']")
    FORM_STATUS = (By.CSS_SELECTOR, "[test-id='form-status']")

    # Модальные окна
    MODAL_OVERLAY = (By.CSS_SELECTOR, "#modal-overlay")
    MODAL_CONTENT = (By.CSS_SELECTOR, ".modal-content")
    MODAL_CLOSE = (By.CSS_SELECTOR, ".modal-close")
    MODAL_BODY = (By.CSS_SELECTOR, "#modal-body")

    # Секции контента
    CONTACT_SECTION = (By.CSS_SELECTOR, ".contact-section")
    SKILLS_SECTION = (By.CSS_SELECTOR, ".skills-section")
    FEEDBACK_SECTION = (By.CSS_SELECTOR, ".feedback-section")

    # Навыки
    SKILL_CATEGORIES = (By.CSS_SELECTOR, ".skill-category")
    SKILL_LISTS = (By.CSS_SELECTOR, ".skill-category ul")


class LoginPageLocators(BaseLocators):
    """Локаторы страницы авторизации (login.html)"""

    # Форма авторизации
    LOGIN_FORM = (By.CSS_SELECTOR, "[test-id='login-form']")
    EMAIL_INPUT = (By.CSS_SELECTOR, "[test-id='email-input']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "[test-id='password-input']")
    LOGIN_SUBMIT_BUTTON = (By.CSS_SELECTOR, "[test-id='login-submit-btn']")
    LOGIN_STATUS = (By.ID, "login-status")

    # Заголовки
    PAGE_TITLE = (By.CSS_SELECTOR, "h2.title")

    # Валидация
    REQUIRED_FIELDS = (By.CSS_SELECTOR, "input[required]")
    EMAIL_FIELD = (By.CSS_SELECTOR, "input[type='email']")
    PASSWORD_FIELD = (By.CSS_SELECTOR, "input[type='password']")


class TestsPageLocators(BaseLocators):
    """Локаторы страницы тестов (tests.html)"""

    # Основные элементы
    PAGE_TITLE = (By.CSS_SELECTOR, "h2.title")
    SIDEBAR = (By.CSS_SELECTOR, ".sidebar")
    CONTENT = (By.CSS_SELECTOR, "#content")

    # Кнопки навигации по компонентам
    INPUTS_TAB = (By.CSS_SELECTOR, "[test-id='inputs-tab']")
    CHECKBOXES_TAB = (By.CSS_SELECTOR, "[test-id='checkboxes-tab']")
    BUTTONS_TAB = (By.CSS_SELECTOR, "[test-id='buttons-tab']")
    IMAGES_TAB = (By.CSS_SELECTOR, "[test-id='images-tab']")
    RADIO_TAB = (By.CSS_SELECTOR, "[test-id='radio-tab']")
    MODALS_TAB = (By.CSS_SELECTOR, "[test-id='modals-tab']")
    SLIDERS_TAB = (By.CSS_SELECTOR, "[test-id='sliders-tab']")
    IFRAMES_TAB = (By.CSS_SELECTOR, "[test-id='iframes-tab']")

    # Демо элементы (появляются после клика на табы)
    DEMO_EMAIL_INPUT = (By.CSS_SELECTOR, "[test-id='demo-email-input']")
    DEMO_LOGIN_INPUT = (By.CSS_SELECTOR, "[test-id='demo-login-input']")
    DEMO_PASSWORD_INPUT = (By.CSS_SELECTOR, "[test-id='demo-password-input']")
    DEMO_COMMENT_TEXTAREA = (By.CSS_SELECTOR, "[test-id='demo-comment-textarea']")
    NORMAL_BUTTON = (By.CSS_SELECTOR, "[test-id='normal-button']")
    DISABLED_BUTTON = (By.CSS_SELECTOR, "[test-id='disabled-button']")
    PRIMARY_BUTTON = (By.CSS_SELECTOR, "[test-id='primary-button']")

    # Кнопки управления чекбоксами
    CHECK_ALL_BTN = (By.CSS_SELECTOR, "[test-id='check-all-btn']")
    UNCHECK_ALL_BTN = (By.CSS_SELECTOR, "[test-id='uncheck-all-btn']")

    # Чекбоксы
    CHECKBOX_1 = (By.CSS_SELECTOR, "[test-id='checkbox-1']")
    CHECKBOX_2 = (By.CSS_SELECTOR, "[test-id='checkbox-2']")
    CHECKBOX_3 = (By.CSS_SELECTOR, "[test-id='checkbox-3']")

    # Заголовки
    PAGE_TITLE = (By.CSS_SELECTOR, "h2.title")

    # Сайдбар
    SIDEBAR = (By.CSS_SELECTOR, ".sidebar")
    SIDEBAR_BUTTONS = (By.CSS_SELECTOR, ".sidebar button")

    # Вкладки сайдбара
    INPUTS_TAB = (By.CSS_SELECTOR, "[test-id='inputs-tab']")
    CHECKBOXES_TAB = (By.CSS_SELECTOR, "[test-id='checkboxes-tab']")
    BUTTONS_TAB = (By.CSS_SELECTOR, "[test-id='buttons-tab']")
    IMAGES_TAB = (By.CSS_SELECTOR, "[test-id='images-tab']")
    RADIO_TAB = (By.CSS_SELECTOR, "[test-id='radio-tab']")
    MODALS_TAB = (By.CSS_SELECTOR, "[test-id='modals-tab']")
    SLIDERS_TAB = (By.CSS_SELECTOR, "[test-id='sliders-tab']")
    IFRAMES_TAB = (By.CSS_SELECTOR, "[test-id='iframes-tab']")

    # Основной контент
    CONTENT_AREA = (By.CSS_SELECTOR, "#content")
    CONTENT_GRID = (By.CSS_SELECTOR, ".grid")
    CONTENT_CARDS = (By.CSS_SELECTOR, ".card")


class InputComponentsLocators:
    """Локаторы компонентов полей ввода"""

    # Демо поля ввода
    DEMO_EMAIL_INPUT = (By.CSS_SELECTOR, "[test-id='demo-email-input']")
    DEMO_LOGIN_INPUT = (By.CSS_SELECTOR, "[test-id='demo-login-input']")
    DEMO_PASSWORD_INPUT = (By.CSS_SELECTOR, "[test-id='demo-password-input']")
    DEMO_COMMENT_TEXTAREA = (By.CSS_SELECTOR, "[test-id='demo-comment-textarea']")

    # Общие селекторы для полей ввода
    ALL_INPUTS = (By.CSS_SELECTOR, "input")
    TEXT_INPUTS = (By.CSS_SELECTOR, "input[type='text']")
    EMAIL_INPUTS = (By.CSS_SELECTOR, "input[type='email']")
    PASSWORD_INPUTS = (By.CSS_SELECTOR, "input[type='password']")
    TEXTAREAS = (By.CSS_SELECTOR, "textarea")

    # Валидация
    REQUIRED_INPUTS = (By.CSS_SELECTOR, "input[required], textarea[required]")


class CheckboxComponentsLocators:
    """Локаторы компонентов чекбоксов"""

    # Демо чекбоксы
    CHECKBOX_1 = (By.CSS_SELECTOR, "[test-id='checkbox-1']")
    CHECKBOX_2 = (By.CSS_SELECTOR, "[test-id='checkbox-2']")
    CHECKBOX_3 = (By.CSS_SELECTOR, "[test-id='checkbox-3']")

    # Кнопки управления
    CHECK_ALL_BUTTON = (By.CSS_SELECTOR, "[test-id='check-all-btn']")
    UNCHECK_ALL_BUTTON = (By.CSS_SELECTOR, "[test-id='uncheck-all-btn']")

    # Общие селекторы
    ALL_CHECKBOXES = (By.CSS_SELECTOR, "input[type='checkbox']")
    CHECKED_CHECKBOXES = (By.CSS_SELECTOR, "input[type='checkbox']:checked")
    UNCHECKED_CHECKBOXES = (By.CSS_SELECTOR, "input[type='checkbox']:not(:checked)")


class ButtonComponentsLocators:
    """Локаторы компонентов кнопок"""

    # Демо кнопки
    NORMAL_BUTTON = (By.CSS_SELECTOR, "[test-id='normal-button']")
    DISABLED_BUTTON = (By.CSS_SELECTOR, "[test-id='disabled-button']")
    PRIMARY_BUTTON = (By.CSS_SELECTOR, "[test-id='primary-button']")

    # Общие селекторы
    ALL_BUTTONS = (By.CSS_SELECTOR, "button")
    ENABLED_BUTTONS = (By.CSS_SELECTOR, "button:not([disabled])")
    DISABLED_BUTTONS = (By.CSS_SELECTOR, "button[disabled]")


class ImageComponentsLocators:
    """Локаторы компонентов изображений"""

    # Демо изображения
    DEMO_IMAGE_1 = (By.CSS_SELECTOR, "[test-id='demo-image-1']")
    DEMO_IMAGE_2 = (By.CSS_SELECTOR, "[test-id='demo-image-2']")
    DEMO_IMAGE_3 = (By.CSS_SELECTOR, "[test-id='demo-image-3']")

    # Общие селекторы
    ALL_IMAGES = (By.CSS_SELECTOR, "img")
    IMAGES_WITH_ALT = (By.CSS_SELECTOR, "img[alt]")


class RadioComponentsLocators:
    """Локаторы компонентов радио кнопок"""

    # Демо радио кнопки
    RADIO_1_1 = (By.CSS_SELECTOR, "[test-id='radio-1-1']")
    RADIO_1_2 = (By.CSS_SELECTOR, "[test-id='radio-1-2']")
    RADIO_1_3 = (By.CSS_SELECTOR, "[test-id='radio-1-3']")
    RADIO_2_A = (By.CSS_SELECTOR, "[test-id='radio-2-a']")
    RADIO_2_B = (By.CSS_SELECTOR, "[test-id='radio-2-b']")

    # Группы радио кнопок
    RADIO_GROUP_1 = (By.CSS_SELECTOR, "input[name='radio1']")
    RADIO_GROUP_2 = (By.CSS_SELECTOR, "input[name='radio2']")

    # Общие селекторы
    ALL_RADIO_BUTTONS = (By.CSS_SELECTOR, "input[type='radio']")
    CHECKED_RADIO_BUTTONS = (By.CSS_SELECTOR, "input[type='radio']:checked")
    UNCHECKED_RADIO_BUTTONS = (By.CSS_SELECTOR, "input[type='radio']:not(:checked)")


class ModalComponentsLocators:
    """Локаторы компонентов модальных окон"""

    # Кнопки открытия модальных окон
    OPEN_MODAL_BUTTON = (By.CSS_SELECTOR, "[test-id='open-modal-btn']")
    OPEN_ALERT_BUTTON = (By.CSS_SELECTOR, "[test-id='open-alert-btn']")
    OPEN_CONFIRM_BUTTON = (By.CSS_SELECTOR, "[test-id='open-confirm-btn']")

    # Модальное окно
    MODAL_OVERLAY = (By.CSS_SELECTOR, "[test-id='modal-overlay']")
    CLOSE_MODAL_BUTTON = (By.CSS_SELECTOR, "[test-id='close-modal-btn']")

    # Общие селекторы
    ALL_MODALS = (By.CSS_SELECTOR, "[role='dialog'], .modal, [test-id*='modal']")


class SliderComponentsLocators:
    """Локаторы компонентов ползунков"""

    # Демо ползунки
    SLIDER_1 = (By.CSS_SELECTOR, "[test-id='slider-1']")
    SLIDER_2 = (By.CSS_SELECTOR, "[test-id='slider-2']")
    SLIDER_3 = (By.CSS_SELECTOR, "[test-id='slider-3']")

    # Общие селекторы
    ALL_SLIDERS = (By.CSS_SELECTOR, "input[type='range']")


class IframeComponentsLocators:
    """Локаторы компонентов iframe"""

    # Демо iframe
    RESUME_IFRAME = (By.CSS_SELECTOR, "[test-id='resume-iframe']")
    LOGIN_IFRAME = (By.CSS_SELECTOR, "[test-id='login-iframe']")

    # Общие селекторы
    ALL_IFRAMES = (By.CSS_SELECTOR, "iframe")


class FormValidationLocators:
    """Локаторы для валидации форм"""

    # Общие селекторы валидации
    REQUIRED_FIELDS = (By.CSS_SELECTOR, "[required]")
    INVALID_FIELDS = (By.CSS_SELECTOR, ":invalid")
    VALID_FIELDS = (By.CSS_SELECTOR, ":valid")

    # Сообщения об ошибках
    ERROR_MESSAGES = (By.CSS_SELECTOR, ".error, .invalid-feedback, [role='alert']")
    SUCCESS_MESSAGES = (By.CSS_SELECTOR, ".success, .valid-feedback")

    # Статусы форм
    FORM_STATUS = (By.CSS_SELECTOR, "[test-id='form-status'], [test-id='login-status']")


# Словарь для быстрого доступа к локаторам по имени
LOCATORS_MAP = {
    "main_page": MainPageLocators,
    "login_page": LoginPageLocators,
    "tests_page": TestsPageLocators,
    "inputs": InputComponentsLocators,
    "checkboxes": CheckboxComponentsLocators,
    "buttons": ButtonComponentsLocators,
    "images": ImageComponentsLocators,
    "radio": RadioComponentsLocators,
    "modals": ModalComponentsLocators,
    "sliders": SliderComponentsLocators,
    "iframes": IframeComponentsLocators,
    "validation": FormValidationLocators,
    "base": BaseLocators,
}


def get_locator(page_name: str, locator_name: str):
    """
    Получить локатор по имени страницы и имени локатора

    Args:
        page_name: Имя страницы (например, 'main_page', 'login_page')
        locator_name: Имя локатора (например, 'EMAIL_INPUT', 'SUBMIT_BUTTON')

    Returns:
        Tuple[By, str]: Локатор в формате (By.SELECTOR, "selector")

    Raises:
        AttributeError: Если локатор не найден
    """
    if page_name not in LOCATORS_MAP:
        raise ValueError(f"Страница '{page_name}' не найдена в LOCATORS_MAP")

    page_class = LOCATORS_MAP[page_name]

    if not hasattr(page_class, locator_name):
        raise AttributeError(
            f"Локатор '{locator_name}' не найден в классе '{page_class.__name__}'"
        )

    return getattr(page_class, locator_name)


def get_all_locators_for_page(page_name: str):
    """
    Получить все локаторы для указанной страницы

    Args:
        page_name: Имя страницы

    Returns:
        dict: Словарь с именами локаторов и их значениями
    """
    if page_name not in LOCATORS_MAP:
        raise ValueError(f"Страница '{page_name}' не найдена в LOCATORS_MAP")

    page_class = LOCATORS_MAP[page_name]
    locators = {}

    for attr_name in dir(page_class):
        if not attr_name.startswith("_") and not callable(
            getattr(page_class, attr_name)
        ):
            locators[attr_name] = getattr(page_class, attr_name)

    return locators
