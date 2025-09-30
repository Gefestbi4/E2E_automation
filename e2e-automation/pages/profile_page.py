from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import Logger
from utils.screenshot import Screenshot
from config.settings import Settings


class ProfilePage(BasePage):
    """
    Page Object для страницы профиля пользователя.
    """

    # Локаторы элементов профиля
    PROFILE_HEADER = (
        By.XPATH,
        "//div[@id='profile-page']/div[@class='page-header']/h1",
    )
    USER_AVATAR = (By.ID, "user-avatar")
    USER_NAME = (By.ID, "user-name")
    USER_EMAIL = (By.ID, "user-email")
    REGISTRATION_DATE = (By.ID, "registration-date")
    USER_STATUS = (By.ID, "user-status")
    ACTIVITY_STATS = (By.ID, "activity-stats")

    # Локаторы для редактирования профиля
    EDIT_PROFILE_BUTTON = (By.ID, "edit-profile-btn")
    FULL_NAME_INPUT = (By.ID, "full-name-input")
    EMAIL_INPUT = (By.ID, "email-input")
    SAVE_PROFILE_BUTTON = (By.ID, "save-profile-btn")
    CANCEL_EDIT_BUTTON = (By.ID, "cancel-edit-btn")

    # Локаторы для смены пароля
    SECURITY_SETTINGS_BUTTON = (By.ID, "security-settings")
    CURRENT_PASSWORD_INPUT = (By.ID, "current-password-input")
    NEW_PASSWORD_INPUT = (By.ID, "new-password-input")
    CONFIRM_PASSWORD_INPUT = (By.ID, "confirm-password-input")
    CHANGE_PASSWORD_BUTTON = (By.ID, "change-password-btn")
    PASSWORD_STRENGTH_INDICATOR = (By.ID, "password-strength")

    # Локаторы для восстановления пароля
    FORGOT_PASSWORD_LINK = (By.ID, "forgot-password-link")
    RESET_EMAIL_INPUT = (By.ID, "reset-email-input")
    SEND_RESET_BUTTON = (By.ID, "send-reset-btn")
    RESET_PASSWORD_FORM = (By.ID, "reset-password-form")
    SAVE_NEW_PASSWORD_BUTTON = (By.ID, "save-new-password-btn")

    # Локаторы для подтверждения email
    EMAIL_VERIFICATION_STATUS = (By.ID, "email-status")
    VERIFY_EMAIL_BUTTON = (By.ID, "verify-email-btn")
    EMAIL_CONFIRMATION_SUCCESS = (By.ID, "email-confirmation-success")

    # Локаторы для настроек уведомлений
    NOTIFICATION_SETTINGS_BUTTON = (By.ID, "notification-settings")
    EMAIL_NOTIFICATIONS_TOGGLE = (By.ID, "email-notifications-toggle")
    PUSH_NOTIFICATIONS_TOGGLE = (By.ID, "push-notifications-toggle")
    NOTIFICATION_TYPES_CHECKBOXES = (
        By.CSS_SELECTOR,
        "input[type='checkbox'][name='notification-types']",
    )
    SAVE_NOTIFICATION_SETTINGS_BUTTON = (By.ID, "save-notification-settings")

    # Локаторы для удаления аккаунта
    ACCOUNT_SETTINGS_BUTTON = (By.ID, "account-settings")
    DELETE_ACCOUNT_BUTTON = (By.ID, "delete-account-btn")
    CONFIRM_DELETION_INPUT = (By.ID, "confirm-deletion-input")
    CONFIRM_DELETE_ACCOUNT_BUTTON = (By.ID, "confirm-delete-account-btn")

    # Локаторы для сообщений
    SUCCESS_MESSAGE = (By.ID, "success-message")
    ERROR_MESSAGE = (By.ID, "error-message")
    VALIDATION_ERROR = (By.CSS_SELECTOR, ".validation-error")

    def __init__(self, driver, logger: Logger, screenshot: Screenshot):
        super().__init__(driver, logger, screenshot)
        self.url = f"{Settings.FRONTEND_URL}#profile"

    def load(self):
        """Загружает страницу профиля."""
        self.driver.get(self.url)
        self.logger.info(f"Загружена страница профиля: {self.url}")
        self._wait_for_element_visible(self.PROFILE_HEADER, "Заголовок профиля")

    def is_profile_loaded(self) -> bool:
        """Проверяет, загружена ли страница профиля."""
        return (
            self._get_element_text(self.PROFILE_HEADER, "Заголовок профиля")
            == "Profile"
        )

    def get_user_name(self) -> str:
        """Возвращает имя пользователя."""
        return self._get_element_text(self.USER_NAME, "Имя пользователя")

    def get_user_email(self) -> str:
        """Возвращает email пользователя."""
        return self._get_element_text(self.USER_EMAIL, "Email пользователя")

    def get_registration_date(self) -> str:
        """Возвращает дату регистрации."""
        return self._get_element_text(self.REGISTRATION_DATE, "Дата регистрации")

    def get_user_status(self) -> str:
        """Возвращает статус пользователя."""
        return self._get_element_text(self.USER_STATUS, "Статус пользователя")

    def get_activity_stats(self) -> str:
        """Возвращает статистику активности."""
        return self._get_element_text(self.ACTIVITY_STATS, "Статистика активности")

    def click_edit_profile(self):
        """Нажимает кнопку редактирования профиля."""
        self._click_element(self.EDIT_PROFILE_BUTTON, "Кнопка 'Редактировать профиль'")

    def edit_full_name(self, new_name: str):
        """Редактирует полное имя пользователя."""
        self.logger.info(f"Редактируем полное имя на: {new_name}")
        self._type_into_element(self.FULL_NAME_INPUT, new_name, "Поле 'Полное имя'")

    def edit_email(self, new_email: str):
        """Редактирует email пользователя."""
        self.logger.info(f"Редактируем email на: {new_email}")
        self._type_into_element(self.EMAIL_INPUT, new_email, "Поле 'Email'")

    def save_profile_changes(self):
        """Сохраняет изменения профиля."""
        self._click_element(self.SAVE_PROFILE_BUTTON, "Кнопка 'Сохранить'")

    def cancel_profile_edit(self):
        """Отменяет редактирование профиля."""
        self._click_element(self.CANCEL_EDIT_BUTTON, "Кнопка 'Отмена'")

    def click_security_settings(self):
        """Переходит в настройки безопасности."""
        self._click_element(self.SECURITY_SETTINGS_BUTTON, "Настройки безопасности")

    def change_password(
        self, current_password: str, new_password: str, confirm_password: str
    ):
        """Меняет пароль пользователя."""
        self.logger.info("Меняем пароль пользователя")
        self._type_into_element(
            self.CURRENT_PASSWORD_INPUT, current_password, "Текущий пароль"
        )
        self._type_into_element(self.NEW_PASSWORD_INPUT, new_password, "Новый пароль")
        self._type_into_element(
            self.CONFIRM_PASSWORD_INPUT, confirm_password, "Подтверждение пароля"
        )
        self._click_element(self.CHANGE_PASSWORD_BUTTON, "Кнопка 'Изменить пароль'")

    def get_password_strength(self) -> str:
        """Возвращает индикатор силы пароля."""
        return self._get_element_text(
            self.PASSWORD_STRENGTH_INDICATOR, "Индикатор силы пароля"
        )

    def click_forgot_password(self):
        """Нажимает ссылку 'Забыли пароль?'."""
        self._click_element(self.FORGOT_PASSWORD_LINK, "Ссылка 'Забыли пароль?'")

    def request_password_reset(self, email: str):
        """Запрашивает восстановление пароля."""
        self.logger.info(f"Запрашиваем восстановление пароля для: {email}")
        self._type_into_element(
            self.RESET_EMAIL_INPUT, email, "Email для восстановления"
        )
        self._click_element(self.SEND_RESET_BUTTON, "Кнопка 'Отправить'")

    def reset_password(self, new_password: str, confirm_password: str):
        """Устанавливает новый пароль."""
        self.logger.info("Устанавливаем новый пароль")
        self._type_into_element(self.NEW_PASSWORD_INPUT, new_password, "Новый пароль")
        self._type_into_element(
            self.CONFIRM_PASSWORD_INPUT, confirm_password, "Подтверждение пароля"
        )
        self._click_element(self.SAVE_NEW_PASSWORD_BUTTON, "Кнопка 'Сохранить пароль'")

    def get_email_verification_status(self) -> str:
        """Возвращает статус подтверждения email."""
        return self._get_element_text(
            self.EMAIL_VERIFICATION_STATUS, "Статус подтверждения email"
        )

    def click_verify_email(self):
        """Нажимает кнопку подтверждения email."""
        self._click_element(self.VERIFY_EMAIL_BUTTON, "Кнопка 'Подтвердить email'")

    def is_email_verification_success(self) -> bool:
        """Проверяет, успешно ли подтвержден email."""
        return self._wait_for_element_visible(
            self.EMAIL_CONFIRMATION_SUCCESS, "Сообщение об успешном подтверждении email"
        )

    def click_notification_settings(self):
        """Переходит в настройки уведомлений."""
        self._click_element(self.NOTIFICATION_SETTINGS_BUTTON, "Настройки уведомлений")

    def toggle_email_notifications(self):
        """Переключает email уведомления."""
        self._click_element(
            self.EMAIL_NOTIFICATIONS_TOGGLE, "Переключатель email уведомлений"
        )

    def toggle_push_notifications(self):
        """Переключает push уведомления."""
        self._click_element(
            self.PUSH_NOTIFICATIONS_TOGGLE, "Переключатель push уведомлений"
        )

    def select_notification_types(self, notification_types: list):
        """Выбирает типы уведомлений."""
        self.logger.info(f"Выбираем типы уведомлений: {notification_types}")
        checkboxes = self.driver.find_elements(*self.NOTIFICATION_TYPES_CHECKBOXES)
        for checkbox in checkboxes:
            notification_type = checkbox.get_attribute("value")
            if notification_type in notification_types:
                if not checkbox.is_selected():
                    checkbox.click()
            else:
                if checkbox.is_selected():
                    checkbox.click()

    def save_notification_settings(self):
        """Сохраняет настройки уведомлений."""
        self._click_element(
            self.SAVE_NOTIFICATION_SETTINGS_BUTTON, "Кнопка 'Сохранить настройки'"
        )

    def click_account_settings(self):
        """Переходит в настройки аккаунта."""
        self._click_element(self.ACCOUNT_SETTINGS_BUTTON, "Настройки аккаунта")

    def click_delete_account(self):
        """Нажимает кнопку удаления аккаунта."""
        self._click_element(self.DELETE_ACCOUNT_BUTTON, "Кнопка 'Удалить аккаунт'")

    def confirm_account_deletion(self):
        """Подтверждает удаление аккаунта."""
        self.logger.info("Подтверждаем удаление аккаунта")
        self._type_into_element(
            self.CONFIRM_DELETION_INPUT, "УДАЛИТЬ", "Подтверждение удаления"
        )
        self._click_element(
            self.CONFIRM_DELETE_ACCOUNT_BUTTON, "Кнопка 'Да, удалить аккаунт'"
        )

    def get_success_message(self) -> str:
        """Возвращает сообщение об успехе."""
        return self._get_element_text(self.SUCCESS_MESSAGE, "Сообщение об успехе")

    def get_error_message(self) -> str:
        """Возвращает сообщение об ошибке."""
        return self._get_element_text(self.ERROR_MESSAGE, "Сообщение об ошибке")

    def get_validation_errors(self) -> list:
        """Возвращает список ошибок валидации."""
        error_elements = self.driver.find_elements(*self.VALIDATION_ERROR)
        return [error.text for error in error_elements]
