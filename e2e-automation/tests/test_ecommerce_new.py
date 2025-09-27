"""
E2E тесты для E-commerce модуля с системой маркировки
"""

import pytest
import allure
from utils.test_markers import debug_test, fixme_test, critical_test, high_priority
from pages.ecommerce.shop_page import ShopPage
from pages.ecommerce.product_page import ProductPage
from pages.ecommerce.cart_page import CartPage
from pages.ecommerce.checkout_page import CheckoutPage
from config.settings import Settings


@allure.feature("E-commerce")
@allure.story("Каталог товаров")
class TestProductCatalog:
    """Тесты каталога товаров"""

    @critical_test("Основной функционал магазина")
    @allure.story("Отображение товаров")
    @pytest.mark.critical
    @pytest.mark.ecommerce
    def test_product_list_display(self, browser, url):
        """Проверка отображения списка товаров"""
        with allure.step("Открытие страницы магазина"):
            shop_page = ShopPage(browser, f"{url}/ecommerce")
            shop_page.open()
            assert shop_page.is_page_loaded(), "Страница магазина не загрузилась"

        with allure.step("Проверка отображения товаров"):
            products = shop_page.get_products()
            assert len(products) > 0, "Товары не отображаются"

            # Проверяем, что каждый товар имеет необходимые элементы
            for product in products:
                assert product.has_name(), "У товара отсутствует название"
                assert product.has_price(), "У товара отсутствует цена"
                assert product.has_image(), "У товара отсутствует изображение"

    @high_priority("Поиск товаров")
    @allure.story("Поиск по каталогу")
    @pytest.mark.high
    @pytest.mark.ecommerce
    def test_product_search(self, browser, url, test_data):
        """Проверка поиска товаров"""
        with allure.step("Открытие страницы магазина"):
            shop_page = ShopPage(browser, f"{url}/ecommerce")
            shop_page.open()

        with allure.step("Поиск товара"):
            search_query = test_data["ecommerce"]["search_query"]
            shop_page.search_products(search_query)

        with allure.step("Проверка результатов поиска"):
            results = shop_page.get_search_results()
            assert len(results) > 0, "Результаты поиска не найдены"

            # Проверяем, что результаты содержат поисковый запрос
            for result in results:
                assert (
                    search_query.lower() in result.get_name().lower()
                ), "Результат не соответствует поисковому запросу"

    @high_priority("Фильтрация товаров")
    @allure.story("Фильтры каталога")
    @pytest.mark.high
    @pytest.mark.ecommerce
    def test_product_filters(self, browser, url):
        """Проверка фильтрации товаров"""
        with allure.step("Открытие страницы магазина"):
            shop_page = ShopPage(browser, f"{url}/ecommerce")
            shop_page.open()

        with allure.step("Применение фильтра по категории"):
            category_filter = "Electronics"
            shop_page.apply_category_filter(category_filter)

        with allure.step("Проверка результатов фильтрации"):
            filtered_products = shop_page.get_products()
            assert len(filtered_products) > 0, "Отфильтрованные товары не найдены"

    @debug_test("Проблема с пагинацией")
    @allure.story("Пагинация")
    @pytest.mark.debug
    @pytest.mark.ecommerce
    def test_product_pagination(self, browser, url):
        """Проверка пагинации товаров"""
        with allure.step("Открытие страницы магазина"):
            shop_page = ShopPage(browser, f"{url}/ecommerce")
            shop_page.open()

        with allure.step("Проверка наличия пагинации"):
            assert shop_page.has_pagination(), "Пагинация отсутствует"

        with allure.step("Переход на следующую страницу"):
            if shop_page.can_go_to_next_page():
                shop_page.go_to_next_page()
                assert (
                    shop_page.is_page_loaded()
                ), "Страница не загрузилась после перехода"

    @fixme_test("Тест падает из-за изменений в API сортировки")
    @allure.story("Сортировка товаров")
    @pytest.mark.fixme
    @pytest.mark.ecommerce
    def test_product_sorting(self, browser, url):
        """Проверка сортировки товаров"""
        with allure.step("Открытие страницы магазина"):
            shop_page = ShopPage(browser, f"{url}/ecommerce")
            shop_page.open()

        with allure.step("Сортировка по цене (по возрастанию)"):
            shop_page.sort_by_price_asc()
            products = shop_page.get_products()

            # Проверяем, что товары отсортированы по цене
            prices = [product.get_price() for product in products]
            assert prices == sorted(
                prices
            ), "Товары не отсортированы по цене (по возрастанию)"


@allure.feature("E-commerce")
@allure.story("Детали товара")
class TestProductDetails:
    """Тесты страницы товара"""

    @critical_test("Критический путь покупки")
    @allure.story("Просмотр товара")
    @pytest.mark.critical
    @pytest.mark.ecommerce
    def test_product_details_display(self, browser, url, test_data):
        """Проверка отображения деталей товара"""
        with allure.step("Открытие страницы товара"):
            product_id = test_data["ecommerce"]["test_product_id"]
            product_page = ProductPage(browser, f"{url}/ecommerce/product/{product_id}")
            product_page.open()
            assert product_page.is_page_loaded(), "Страница товара не загрузилась"

        with allure.step("Проверка отображения информации о товаре"):
            assert product_page.has_product_name(), "Название товара не отображается"
            assert product_page.has_product_price(), "Цена товара не отображается"
            assert (
                product_page.has_product_description()
            ), "Описание товара не отображается"
            assert (
                product_page.has_product_images()
            ), "Изображения товара не отображаются"

    @high_priority("Добавление в корзину")
    @allure.story("Корзина покупок")
    @pytest.mark.high
    @pytest.mark.ecommerce
    def test_add_to_cart(self, browser, url, test_data):
        """Проверка добавления товара в корзину"""
        with allure.step("Открытие страницы товара"):
            product_id = test_data["ecommerce"]["test_product_id"]
            product_page = ProductPage(browser, f"{url}/ecommerce/product/{product_id}")
            product_page.open()

        with allure.step("Добавление товара в корзину"):
            initial_cart_count = product_page.get_cart_count()
            product_page.add_to_cart()

            # Ждем обновления счетчика корзины
            product_page.wait_for_cart_update()

        with allure.step("Проверка обновления корзины"):
            new_cart_count = product_page.get_cart_count()
            assert (
                new_cart_count == initial_cart_count + 1
            ), "Товар не добавлен в корзину"

    @high_priority("Выбор вариантов товара")
    @allure.story("Варианты товара")
    @pytest.mark.high
    @pytest.mark.ecommerce
    def test_product_variants(self, browser, url, test_data):
        """Проверка выбора вариантов товара (размер, цвет)"""
        with allure.step("Открытие страницы товара с вариантами"):
            product_id = test_data["ecommerce"]["variant_product_id"]
            product_page = ProductPage(browser, f"{url}/ecommerce/product/{product_id}")
            product_page.open()

        with allure.step("Выбор варианта товара"):
            if product_page.has_variants():
                product_page.select_variant("size", "L")
                product_page.select_variant("color", "Red")

                selected_variants = product_page.get_selected_variants()
                assert "size" in selected_variants, "Размер не выбран"
                assert "color" in selected_variants, "Цвет не выбран"

    @medium_priority("Отзывы о товаре")
    @allure.story("Отзывы")
    @pytest.mark.medium
    @pytest.mark.ecommerce
    def test_product_reviews(self, browser, url, test_data):
        """Проверка отображения отзывов о товаре"""
        with allure.step("Открытие страницы товара"):
            product_id = test_data["ecommerce"]["test_product_id"]
            product_page = ProductPage(browser, f"{url}/ecommerce/product/{product_id}")
            product_page.open()

        with allure.step("Проверка отображения отзывов"):
            if product_page.has_reviews_section():
                reviews = product_page.get_reviews()
                assert len(reviews) > 0, "Отзывы не отображаются"

                # Проверяем структуру отзыва
                for review in reviews:
                    assert review.has_rating(), "У отзыва отсутствует рейтинг"
                    assert review.has_text(), "У отзыва отсутствует текст"

    @debug_test("Проблема с загрузкой изображений")
    @allure.story("Галерея изображений")
    @pytest.mark.debug
    @pytest.mark.ecommerce
    def test_product_image_gallery(self, browser, url, test_data):
        """Проверка галереи изображений товара"""
        with allure.step("Открытие страницы товара"):
            product_id = test_data["ecommerce"]["test_product_id"]
            product_page = ProductPage(browser, f"{url}/ecommerce/product/{product_id}")
            product_page.open()

        with allure.step("Проверка главного изображения"):
            assert product_page.has_main_image(), "Главное изображение не отображается"

            main_image_src = product_page.get_main_image_src()
            assert main_image_src, "URL главного изображения отсутствует"

        with allure.step("Проверка миниатюр"):
            if product_page.has_thumbnails():
                thumbnails = product_page.get_thumbnails()
                assert len(thumbnails) > 1, "Миниатюры не отображаются"

                # Клик по миниатюре
                product_page.click_thumbnail(1)
                new_main_image = product_page.get_main_image_src()
                assert (
                    new_main_image != main_image_src
                ), "Изображение не изменилось после клика по миниатюре"


@allure.feature("E-commerce")
@allure.story("Корзина покупок")
class TestShoppingCart:
    """Тесты корзины покупок"""

    @critical_test("Критический путь покупки")
    @allure.story("Управление корзиной")
    @pytest.mark.critical
    @pytest.mark.ecommerce
    def test_cart_management(self, browser, url, test_data):
        """Проверка управления товарами в корзине"""
        with allure.step("Добавление товара в корзину"):
            product_id = test_data["ecommerce"]["test_product_id"]
            product_page = ProductPage(browser, f"{url}/ecommerce/product/{product_id}")
            product_page.open()
            product_page.add_to_cart()

        with allure.step("Переход в корзину"):
            cart_page = CartPage(browser, f"{url}/ecommerce/cart")
            cart_page.open()
            assert cart_page.is_page_loaded(), "Страница корзины не загрузилась"

        with allure.step("Проверка отображения товара в корзине"):
            cart_items = cart_page.get_cart_items()
            assert len(cart_items) > 0, "Товары в корзине не отображаются"

            cart_item = cart_items[0]
            assert cart_item.has_product_name(), "Название товара в корзине отсутствует"
            assert cart_item.has_product_price(), "Цена товара в корзине отсутствует"
            assert cart_item.has_quantity_selector(), "Селектор количества отсутствует"

    @high_priority("Изменение количества")
    @allure.story("Количество товаров")
    @pytest.mark.high
    @pytest.mark.ecommerce
    def test_quantity_update(self, browser, url, test_data):
        """Проверка изменения количества товара в корзине"""
        with allure.step("Добавление товара в корзину"):
            product_id = test_data["ecommerce"]["test_product_id"]
            product_page = ProductPage(browser, f"{url}/ecommerce/product/{product_id}")
            product_page.open()
            product_page.add_to_cart()

        with allure.step("Переход в корзину"):
            cart_page = CartPage(browser, f"{url}/ecommerce/cart")
            cart_page.open()

        with allure.step("Изменение количества товара"):
            initial_quantity = cart_page.get_item_quantity(0)
            cart_page.update_item_quantity(0, 3)

            new_quantity = cart_page.get_item_quantity(0)
            assert new_quantity == 3, "Количество товара не изменилось"

        with allure.step("Проверка обновления общей стоимости"):
            cart_page.wait_for_total_update()
            total = cart_page.get_cart_total()
            assert total > 0, "Общая стоимость не обновилась"

    @high_priority("Удаление из корзины")
    @allure.story("Удаление товаров")
    @pytest.mark.high
    @pytest.mark.ecommerce
    def test_remove_from_cart(self, browser, url, test_data):
        """Проверка удаления товара из корзины"""
        with allure.step("Добавление товара в корзину"):
            product_id = test_data["ecommerce"]["test_product_id"]
            product_page = ProductPage(browser, f"{url}/ecommerce/product/{product_id}")
            product_page.open()
            product_page.add_to_cart()

        with allure.step("Переход в корзину"):
            cart_page = CartPage(browser, f"{url}/ecommerce/cart")
            cart_page.open()

        with allure.step("Удаление товара из корзины"):
            initial_items_count = len(cart_page.get_cart_items())
            cart_page.remove_item(0)

            cart_page.wait_for_cart_update()
            new_items_count = len(cart_page.get_cart_items())
            assert (
                new_items_count == initial_items_count - 1
            ), "Товар не удален из корзины"

    @medium_priority("Применение промокода")
    @allure.story("Промокоды")
    @pytest.mark.medium
    @pytest.mark.ecommerce
    def test_promo_code(self, browser, url, test_data):
        """Проверка применения промокода"""
        with allure.step("Добавление товара в корзину"):
            product_id = test_data["ecommerce"]["test_product_id"]
            product_page = ProductPage(browser, f"{url}/ecommerce/product/{product_id}")
            product_page.open()
            product_page.add_to_cart()

        with allure.step("Переход в корзину"):
            cart_page = CartPage(browser, f"{url}/ecommerce/cart")
            cart_page.open()

        with allure.step("Применение промокода"):
            promo_code = test_data["ecommerce"]["valid_promo_code"]
            initial_total = cart_page.get_cart_total()

            cart_page.apply_promo_code(promo_code)
            cart_page.wait_for_total_update()

            new_total = cart_page.get_cart_total()
            assert new_total < initial_total, "Промокод не применен"

    @debug_test("Проблема с валидацией промокода")
    @allure.story("Неверный промокод")
    @pytest.mark.debug
    @pytest.mark.ecommerce
    def test_invalid_promo_code(self, browser, url, test_data):
        """Проверка обработки неверного промокода"""
        with allure.step("Добавление товара в корзину"):
            product_id = test_data["ecommerce"]["test_product_id"]
            product_page = ProductPage(browser, f"{url}/ecommerce/product/{product_id}")
            product_page.open()
            product_page.add_to_cart()

        with allure.step("Переход в корзину"):
            cart_page = CartPage(browser, f"{url}/ecommerce/cart")
            cart_page.open()

        with allure.step("Применение неверного промокода"):
            invalid_promo = "INVALID_CODE"
            cart_page.apply_promo_code(invalid_promo)

            # Проверяем отображение ошибки
            assert (
                cart_page.is_promo_error_displayed()
            ), "Ошибка промокода не отображается"


@allure.feature("E-commerce")
@allure.story("Оформление заказа")
class TestCheckout:
    """Тесты оформления заказа"""

    @critical_test("Критический путь покупки")
    @allure.story("Полный процесс покупки")
    @pytest.mark.critical
    @pytest.mark.ecommerce
    def test_complete_purchase_flow(self, browser, url, test_data):
        """Проверка полного процесса покупки"""
        with allure.step("Добавление товара в корзину"):
            product_id = test_data["ecommerce"]["test_product_id"]
            product_page = ProductPage(browser, f"{url}/ecommerce/product/{product_id}")
            product_page.open()
            product_page.add_to_cart()

        with allure.step("Переход к оформлению заказа"):
            cart_page = CartPage(browser, f"{url}/ecommerce/cart")
            cart_page.open()
            cart_page.proceed_to_checkout()

        with allure.step("Заполнение данных для доставки"):
            checkout_page = CheckoutPage(browser, f"{url}/ecommerce/checkout")
            assert (
                checkout_page.is_page_loaded()
            ), "Страница оформления заказа не загрузилась"

            shipping_data = test_data["ecommerce"]["shipping_data"]
            checkout_page.fill_shipping_form(shipping_data)

        with allure.step("Выбор способа оплаты"):
            checkout_page.select_payment_method("credit_card")

        with allure.step("Заполнение данных карты"):
            payment_data = test_data["ecommerce"]["payment_data"]
            checkout_page.fill_payment_form(payment_data)

        with allure.step("Подтверждение заказа"):
            checkout_page.place_order()

            # Проверяем успешное оформление заказа
            assert checkout_page.is_order_successful(), "Заказ не оформлен успешно"

            order_number = checkout_page.get_order_number()
            assert order_number, "Номер заказа не получен"

    @high_priority("Валидация формы")
    @allure.story("Валидация данных")
    @pytest.mark.high
    @pytest.mark.ecommerce
    def test_checkout_form_validation(self, browser, url, test_data):
        """Проверка валидации формы оформления заказа"""
        with allure.step("Добавление товара в корзину"):
            product_id = test_data["ecommerce"]["test_product_id"]
            product_page = ProductPage(browser, f"{url}/ecommerce/product/{product_id}")
            product_page.open()
            product_page.add_to_cart()

        with allure.step("Переход к оформлению заказа"):
            cart_page = CartPage(browser, f"{url}/ecommerce/cart")
            cart_page.open()
            cart_page.proceed_to_checkout()

        with allure.step("Попытка оформления без заполнения полей"):
            checkout_page = CheckoutPage(browser, f"{url}/ecommerce/checkout")
            checkout_page.place_order()

            # Проверяем отображение ошибок валидации
            assert (
                checkout_page.has_validation_errors()
            ), "Ошибки валидации не отображаются"

    @medium_priority("Способы доставки")
    @allure.story("Доставка")
    @pytest.mark.medium
    @pytest.mark.ecommerce
    def test_shipping_options(self, browser, url, test_data):
        """Проверка выбора способов доставки"""
        with allure.step("Добавление товара в корзину"):
            product_id = test_data["ecommerce"]["test_product_id"]
            product_page = ProductPage(browser, f"{url}/ecommerce/product/{product_id}")
            product_page.open()
            product_page.add_to_cart()

        with allure.step("Переход к оформлению заказа"):
            cart_page = CartPage(browser, f"{url}/ecommerce/cart")
            cart_page.open()
            cart_page.proceed_to_checkout()

        with allure.step("Проверка доступных способов доставки"):
            checkout_page = CheckoutPage(browser, f"{url}/ecommerce/checkout")
            shipping_options = checkout_page.get_shipping_options()
            assert len(shipping_options) > 0, "Способы доставки не отображаются"

            # Выбор способа доставки
            checkout_page.select_shipping_method(shipping_options[0])

            # Проверяем обновление стоимости
            checkout_page.wait_for_total_update()
            total = checkout_page.get_order_total()
            assert total > 0, "Общая стоимость заказа не обновилась"

    @fixme_test("Тест падает из-за проблем с платежной системой")
    @allure.story("Оплата")
    @pytest.mark.fixme
    @pytest.mark.ecommerce
    def test_payment_processing(self, browser, url, test_data):
        """Проверка обработки платежей"""
        # Этот тест сломан и требует исправления
        # Проблема связана с интеграцией платежной системы
        pass
