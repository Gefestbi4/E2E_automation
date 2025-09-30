from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import Logger
from utils.screenshot import Screenshot
from config.settings import Settings


class CartPage(BasePage):
    """
    Page Object для страницы корзины покупок.
    """

    # Локаторы элементов корзины
    CART_HEADER = (By.XPATH, "//div[@id='cart-page']/div[@class='page-header']/h1")
    CART_ITEMS = (By.ID, "cart-items")
    CART_ITEM = (By.CSS_SELECTOR, ".cart-item")
    CART_TOTAL = (By.ID, "cart-total")
    CART_COUNTER = (By.ID, "cart-counter")

    # Локаторы для товаров в корзине
    ITEM_NAME = (By.CSS_SELECTOR, ".cart-item .item-name")
    ITEM_PRICE = (By.CSS_SELECTOR, ".cart-item .item-price")
    ITEM_QUANTITY_INPUT = (By.CSS_SELECTOR, ".cart-item .quantity-input")
    QUANTITY_INCREASE_BUTTON = (By.CSS_SELECTOR, ".cart-item .quantity-increase")
    QUANTITY_DECREASE_BUTTON = (By.CSS_SELECTOR, ".cart-item .quantity-decrease")
    REMOVE_ITEM_BUTTON = (By.CSS_SELECTOR, ".cart-item .remove-item-btn")

    # Локаторы для управления корзиной
    CLEAR_CART_BUTTON = (By.ID, "clear-cart-btn")
    CONFIRM_CLEAR_BUTTON = (By.ID, "confirm-clear-btn")
    EMPTY_CART_MESSAGE = (By.ID, "empty-cart-message")

    # Локаторы для промокодов
    PROMO_CODE_INPUT = (By.ID, "promo-code-input")
    APPLY_PROMO_BUTTON = (By.ID, "apply-promo-btn")
    PROMO_CODE_ERROR = (By.ID, "promo-code-error")
    DISCOUNT_AMOUNT = (By.ID, "discount-amount")

    # Локаторы для оформления заказа
    CHECKOUT_BUTTON = (By.ID, "checkout-btn")
    CONTINUE_SHOPPING_BUTTON = (By.ID, "continue-shopping-btn")

    # Локаторы для уведомлений
    CART_NOTIFICATION = (By.ID, "cart-notification")
    SUCCESS_MESSAGE = (By.ID, "success-message")
    ERROR_MESSAGE = (By.ID, "error-message")

    def __init__(self, driver, logger: Logger, screenshot: Screenshot):
        super().__init__(driver, logger, screenshot)
        self.url = f"{Settings.FRONTEND_URL}#cart"

    def load(self):
        """Загружает страницу корзины."""
        self.driver.get(self.url)
        self.logger.info(f"Загружена страница корзины: {self.url}")
        self._wait_for_element_visible(self.CART_HEADER, "Заголовок корзины")

    def is_cart_loaded(self) -> bool:
        """Проверяет, загружена ли страница корзины."""
        return (
            self._get_element_text(self.CART_HEADER, "Заголовок корзины")
            == "Shopping Cart"
        )

    def get_cart_items(self) -> list:
        """Возвращает список товаров в корзине."""
        self.logger.info("Получаем список товаров в корзине")
        return self.driver.find_elements(*self.CART_ITEM)

    def get_cart_total(self) -> str:
        """Возвращает общую сумму корзины."""
        return self._get_element_text(self.CART_TOTAL, "Общая сумма корзины")

    def get_cart_counter(self) -> int:
        """Возвращает количество товаров в корзине."""
        try:
            counter_text = self._get_element_text(self.CART_COUNTER, "Счетчик корзины")
            return int(counter_text)
        except ValueError:
            self.logger.warning(
                "Не удалось преобразовать текст счетчика корзины в число"
            )
            return 0

    def get_item_name(self, item_index: int = 0) -> str:
        """Возвращает название товара по индексу."""
        items = self.get_cart_items()
        if item_index < len(items):
            return items[item_index].find_element(*self.ITEM_NAME).text
        return ""

    def get_item_price(self, item_index: int = 0) -> str:
        """Возвращает цену товара по индексу."""
        items = self.get_cart_items()
        if item_index < len(items):
            return items[item_index].find_element(*self.ITEM_PRICE).text
        return ""

    def get_item_quantity(self, item_index: int = 0) -> int:
        """Возвращает количество товара по индексу."""
        items = self.get_cart_items()
        if item_index < len(items):
            quantity_input = items[item_index].find_element(*self.ITEM_QUANTITY_INPUT)
            return int(quantity_input.get_attribute("value"))
        return 0

    def change_item_quantity(self, item_index: int, new_quantity: int):
        """Изменяет количество товара."""
        self.logger.info(f"Изменяем количество товара {item_index} на {new_quantity}")
        items = self.get_cart_items()
        if item_index < len(items):
            quantity_input = items[item_index].find_element(*self.ITEM_QUANTITY_INPUT)
            quantity_input.clear()
            quantity_input.send_keys(str(new_quantity))
            # Триггер события change
            self.driver.execute_script(
                "arguments[0].dispatchEvent(new Event('change'));", quantity_input
            )

    def increase_item_quantity(self, item_index: int):
        """Увеличивает количество товара на 1."""
        self.logger.info(f"Увеличиваем количество товара {item_index}")
        items = self.get_cart_items()
        if item_index < len(items):
            increase_button = items[item_index].find_element(
                *self.QUANTITY_INCREASE_BUTTON
            )
            increase_button.click()

    def decrease_item_quantity(self, item_index: int):
        """Уменьшает количество товара на 1."""
        self.logger.info(f"Уменьшаем количество товара {item_index}")
        items = self.get_cart_items()
        if item_index < len(items):
            decrease_button = items[item_index].find_element(
                *self.QUANTITY_DECREASE_BUTTON
            )
            decrease_button.click()

    def remove_item(self, item_index: int):
        """Удаляет товар из корзины."""
        self.logger.info(f"Удаляем товар {item_index} из корзины")
        items = self.get_cart_items()
        if item_index < len(items):
            remove_button = items[item_index].find_element(*self.REMOVE_ITEM_BUTTON)
            remove_button.click()

    def click_clear_cart(self):
        """Нажимает кнопку очистки корзины."""
        self._click_element(self.CLEAR_CART_BUTTON, "Кнопка 'Очистить корзину'")

    def confirm_clear_cart(self):
        """Подтверждает очистку корзины."""
        self._click_element(self.CONFIRM_CLEAR_BUTTON, "Кнопка 'Да, очистить корзину'")

    def is_cart_empty(self) -> bool:
        """Проверяет, пуста ли корзина."""
        try:
            self._wait_for_element_visible(
                self.EMPTY_CART_MESSAGE, "Сообщение о пустой корзине"
            )
            return True
        except:
            return False

    def apply_promo_code(self, promo_code: str):
        """Применяет промокод."""
        self.logger.info(f"Применяем промокод: {promo_code}")
        self._type_into_element(self.PROMO_CODE_INPUT, promo_code, "Поле промокода")
        self._click_element(self.APPLY_PROMO_BUTTON, "Кнопка 'Применить промокод'")

    def get_promo_code_error(self) -> str:
        """Возвращает ошибку промокода."""
        return self._get_element_text(self.PROMO_CODE_ERROR, "Ошибка промокода")

    def get_discount_amount(self) -> str:
        """Возвращает размер скидки."""
        return self._get_element_text(self.DISCOUNT_AMOUNT, "Размер скидки")

    def click_checkout(self):
        """Нажимает кнопку оформления заказа."""
        self._click_element(self.CHECKOUT_BUTTON, "Кнопка 'Оформить заказ'")

    def click_continue_shopping(self):
        """Нажимает кнопку продолжить покупки."""
        self._click_element(
            self.CONTINUE_SHOPPING_BUTTON, "Кнопка 'Продолжить покупки'"
        )

    def get_cart_notification(self) -> str:
        """Возвращает уведомление корзины."""
        try:
            self._wait_for_element_visible(
                self.CART_NOTIFICATION, "Уведомление корзины"
            )
            notification_text = self._get_element_text(
                self.CART_NOTIFICATION, "Текст уведомления корзины"
            )
            self._wait_for_element_invisible(
                self.CART_NOTIFICATION, "Уведомление корзины"
            )
            return notification_text
        except:
            return ""

    def get_success_message(self) -> str:
        """Возвращает сообщение об успехе."""
        return self._get_element_text(self.SUCCESS_MESSAGE, "Сообщение об успехе")

    def get_error_message(self) -> str:
        """Возвращает сообщение об ошибке."""
        return self._get_element_text(self.ERROR_MESSAGE, "Сообщение об ошибке")

    def is_item_in_cart(self, item_name: str) -> bool:
        """Проверяет, есть ли товар в корзине."""
        items = self.get_cart_items()
        for item in items:
            if item.find_element(*self.ITEM_NAME).text == item_name:
                return True
        return False

    def get_item_count_by_name(self, item_name: str) -> int:
        """Возвращает количество товара по названию."""
        items = self.get_cart_items()
        for item in items:
            if item.find_element(*self.ITEM_NAME).text == item_name:
                quantity_input = item.find_element(*self.ITEM_QUANTITY_INPUT)
                return int(quantity_input.get_attribute("value"))
        return 0
