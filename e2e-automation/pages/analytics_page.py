from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import Logger
from utils.screenshot import Screenshot
from config.settings import Settings


class AnalyticsPage(BasePage):
    """
    Page Object для страницы аналитики и дашборда.
    """

    # Локаторы элементов аналитики
    ANALYTICS_HEADER = (
        By.XPATH,
        "//div[@id='analytics-page']/div[@class='page-header']/h1",
    )
    METRICS_CARDS = (By.ID, "metrics-cards")
    CHARTS_CONTAINER = (By.ID, "charts-container")
    ACTIVITY_FEED = (By.ID, "activity-feed")

    # Локаторы для метрик пользователей
    USERS_METRIC = (By.ID, "users-metric")
    USERS_DETAILS = (By.ID, "users-details")
    USERS_GROWTH_CHART = (By.ID, "users-growth-chart")

    # Локаторы для метрик E-commerce
    PRODUCTS_METRIC = (By.ID, "products-metric")
    ORDERS_METRIC = (By.ID, "orders-metric")
    REVENUE_METRIC = (By.ID, "revenue-metric")
    REVENUE_CHART = (By.ID, "revenue-chart")

    # Локаторы для активности системы
    RECENT_ACTIVITY = (By.ID, "recent-activity")
    ACTIVITY_ITEM = (By.CSS_SELECTOR, ".activity-item")

    # Локаторы для настройки виджетов
    CUSTOMIZE_DASHBOARD_BUTTON = (By.ID, "customize-dashboard-btn")
    WIDGET_CARD = (By.CSS_SELECTOR, ".widget-card")
    RESIZE_WIDGET = (By.CSS_SELECTOR, ".resize-widget")
    SAVE_DASHBOARD_BUTTON = (By.ID, "save-dashboard-btn")

    # Локаторы для создания пользовательского дашборда
    CREATE_DASHBOARD_BUTTON = (By.ID, "create-dashboard-btn")
    DASHBOARD_NAME_INPUT = (By.ID, "dashboard-name-input")
    WIDGET_SELECTOR = (By.ID, "widget-selector")
    CREATE_DASHBOARD_SUBMIT = (By.ID, "create-dashboard-submit")

    # Локаторы для графиков
    USER_GROWTH_CHART = (By.ID, "user-growth-chart")
    CHART_TOOLTIP = (By.CSS_SELECTOR, ".chart-tooltip")
    TIME_PERIOD_SELECT = (By.ID, "time-period-select")
    CHART_TYPE_SELECT = (By.ID, "chart-type-select")

    # Локаторы для фильтрации по дате
    DATE_RANGE_SELECT = (By.ID, "date-range-select")
    CUSTOM_DATE_PICKER = (By.ID, "custom-date-picker")
    APPLY_DATE_FILTER_BUTTON = (By.ID, "apply-date-filter-btn")

    # Локаторы для экспорта данных
    EXPORT_REPORT_BUTTON = (By.ID, "export-report-btn")
    EXPORT_FORMAT_SELECT = (By.ID, "export-format-select")
    DOWNLOAD_REPORT_BUTTON = (By.ID, "download-report-btn")

    # Локаторы для автообновления
    AUTO_REFRESH_BUTTON = (By.ID, "auto-refresh-btn")

    # Локаторы для переключения дашбордов
    DASHBOARD_SELECTOR = (By.ID, "dashboard-selector")
    ECOMMERCE_DASHBOARD = (By.ID, "ecommerce-dashboard")

    # Локаторы для уведомлений
    SUCCESS_MESSAGE = (By.ID, "success-message")
    ERROR_MESSAGE = (By.ID, "error-message")

    def __init__(self, driver, logger: Logger, screenshot: Screenshot):
        super().__init__(driver, logger, screenshot)
        self.url = f"{Settings.FRONTEND_URL}#analytics"

    def load(self):
        """Загружает страницу аналитики."""
        self.driver.get(self.url)
        self.logger.info(f"Загружена страница аналитики: {self.url}")
        self._wait_for_element_visible(self.ANALYTICS_HEADER, "Заголовок аналитики")

    def is_analytics_loaded(self) -> bool:
        """Проверяет, загружена ли страница аналитики."""
        return (
            self._get_element_text(self.ANALYTICS_HEADER, "Заголовок аналитики")
            == "Analytics"
        )

    def get_metrics_cards(self) -> list:
        """Возвращает список карточек метрик."""
        self.logger.info("Получаем список карточек метрик")
        return self.driver.find_elements(*self.METRICS_CARDS)

    def get_users_metric(self) -> str:
        """Возвращает метрику пользователей."""
        return self._get_element_text(self.USERS_METRIC, "Метрика пользователей")

    def click_users_metric(self):
        """Кликает на метрику пользователей для детальной информации."""
        self._click_element(self.USERS_METRIC, "Метрика пользователей")

    def get_users_details(self) -> str:
        """Возвращает детальную информацию о пользователях."""
        return self._get_element_text(
            self.USERS_DETAILS, "Детальная информация о пользователях"
        )

    def get_users_growth_chart(self) -> str:
        """Возвращает график роста пользователей."""
        return self._get_element_text(
            self.USERS_GROWTH_CHART, "График роста пользователей"
        )

    def get_products_metric(self) -> str:
        """Возвращает метрику товаров."""
        return self._get_element_text(self.PRODUCTS_METRIC, "Метрика товаров")

    def get_orders_metric(self) -> str:
        """Возвращает метрику заказов."""
        return self._get_element_text(self.ORDERS_METRIC, "Метрика заказов")

    def get_revenue_metric(self) -> str:
        """Возвращает метрику выручки."""
        return self._get_element_text(self.REVENUE_METRIC, "Метрика выручки")

    def get_revenue_chart(self) -> str:
        """Возвращает график выручки."""
        return self._get_element_text(self.REVENUE_CHART, "График выручки")

    def get_recent_activity(self) -> list:
        """Возвращает список последней активности."""
        self.logger.info("Получаем список последней активности")
        return self.driver.find_elements(*self.ACTIVITY_ITEM)

    def get_activity_item(self, activity_index: int = 0) -> str:
        """Возвращает элемент активности по индексу."""
        activities = self.get_recent_activity()
        if activity_index < len(activities):
            return activities[activity_index].text
        return ""

    def click_customize_dashboard(self):
        """Нажимает кнопку настройки дашборда."""
        self._click_element(
            self.CUSTOMIZE_DASHBOARD_BUTTON, "Кнопка 'Настроить панель'"
        )

    def get_widget_cards(self) -> list:
        """Возвращает список виджетов."""
        return self.driver.find_elements(*self.WIDGET_CARD)

    def resize_widget(self, widget_index: int):
        """Изменяет размер виджета."""
        self.logger.info(f"Изменяем размер виджета {widget_index}")
        widgets = self.get_widget_cards()
        if widget_index < len(widgets):
            resize_handle = widgets[widget_index].find_element(*self.RESIZE_WIDGET)
            # Используем ActionChains для изменения размера
            from selenium.webdriver.common.action_chains import ActionChains

            ActionChains(self.driver).drag_and_drop_by_offset(
                resize_handle, 50, 50
            ).perform()

    def save_dashboard(self):
        """Сохраняет настройки дашборда."""
        self._click_element(self.SAVE_DASHBOARD_BUTTON, "Кнопка 'Сохранить'")

    def click_create_dashboard(self):
        """Нажимает кнопку создания дашборда."""
        self._click_element(self.CREATE_DASHBOARD_BUTTON, "Кнопка 'Создать дашборд'")

    def create_custom_dashboard(self, name: str, widgets: list):
        """Создает пользовательский дашборд."""
        self.logger.info(f"Создаем пользовательский дашборд: {name}")
        self._type_into_element(self.DASHBOARD_NAME_INPUT, name, "Название дашборда")

        # Выбираем виджеты
        for widget in widgets:
            self._find_element(self.WIDGET_SELECTOR, "Выбор виджетов").send_keys(widget)

        self._click_element(self.CREATE_DASHBOARD_SUBMIT, "Кнопка 'Создать'")

    def get_user_growth_chart(self) -> str:
        """Возвращает график роста пользователей."""
        return self._get_element_text(
            self.USER_GROWTH_CHART, "График роста пользователей"
        )

    def hover_chart_point(self, chart_index: int = 0):
        """Наводит курсор на точку графика."""
        self.logger.info(f"Наводим курсор на точку графика {chart_index}")
        charts = self.driver.find_elements(*self.USER_GROWTH_CHART)
        if chart_index < len(charts):
            from selenium.webdriver.common.action_chains import ActionChains

            ActionChains(self.driver).move_to_element(charts[chart_index]).perform()

    def get_chart_tooltip(self) -> str:
        """Возвращает всплывающую подсказку графика."""
        return self._get_element_text(
            self.CHART_TOOLTIP, "Всплывающая подсказка графика"
        )

    def change_time_period(self, period: str):
        """Изменяет период отображения данных."""
        self.logger.info(f"Изменяем период отображения на: {period}")
        self._find_element(self.TIME_PERIOD_SELECT, "Выбор периода времени").send_keys(
            period
        )

    def change_chart_type(self, chart_type: str):
        """Изменяет тип графика."""
        self.logger.info(f"Изменяем тип графика на: {chart_type}")
        self._find_element(self.CHART_TYPE_SELECT, "Выбор типа графика").send_keys(
            chart_type
        )

    def select_date_range(self, date_range: str):
        """Выбирает диапазон дат."""
        self.logger.info(f"Выбираем диапазон дат: {date_range}")
        self._find_element(self.DATE_RANGE_SELECT, "Выбор диапазона дат").send_keys(
            date_range
        )

    def select_custom_date_range(self, start_date: str, end_date: str):
        """Выбирает кастомный диапазон дат."""
        self.logger.info(f"Выбираем кастомный диапазон дат: {start_date} - {end_date}")
        self._click_element(self.CUSTOM_DATE_PICKER, "Выбор кастомных дат")
        # Здесь можно добавить логику для выбора дат в календаре
        self._click_element(self.APPLY_DATE_FILTER_BUTTON, "Кнопка 'Применить'")

    def click_export_report(self):
        """Нажимает кнопку экспорта отчета."""
        self._click_element(self.EXPORT_REPORT_BUTTON, "Кнопка 'Экспорт отчета'")

    def select_export_format(self, format_type: str):
        """Выбирает формат экспорта."""
        self.logger.info(f"Выбираем формат экспорта: {format_type}")
        self._find_element(
            self.EXPORT_FORMAT_SELECT, "Выбор формата экспорта"
        ).send_keys(format_type)

    def download_report(self):
        """Скачивает отчет."""
        self._click_element(self.DOWNLOAD_REPORT_BUTTON, "Кнопка 'Скачать'")

    def toggle_auto_refresh(self):
        """Переключает автообновление."""
        self._click_element(self.AUTO_REFRESH_BUTTON, "Кнопка 'Автообновление'")

    def is_auto_refresh_enabled(self) -> bool:
        """Проверяет, включено ли автообновление."""
        button = self._find_element(self.AUTO_REFRESH_BUTTON, "Кнопка автообновления")
        return "active" in button.get_attribute("class")

    def select_dashboard(self, dashboard_name: str):
        """Выбирает дашборд из списка."""
        self.logger.info(f"Выбираем дашборд: {dashboard_name}")
        self._click_element(self.DASHBOARD_SELECTOR, "Выбор дашборда")
        self._find_element(self.DASHBOARD_SELECTOR, "Выбор дашборда").send_keys(
            dashboard_name
        )

    def select_ecommerce_dashboard(self):
        """Выбирает E-commerce дашборд."""
        self._click_element(self.ECOMMERCE_DASHBOARD, "E-commerce дашборд")

    def get_success_message(self) -> str:
        """Возвращает сообщение об успехе."""
        return self._get_element_text(self.SUCCESS_MESSAGE, "Сообщение об успехе")

    def get_error_message(self) -> str:
        """Возвращает сообщение об ошибке."""
        return self._get_element_text(self.ERROR_MESSAGE, "Сообщение об ошибке")

    def is_metric_visible(self, metric_name: str) -> bool:
        """Проверяет, видна ли метрика."""
        try:
            metric_element = self._find_element(
                (By.ID, f"{metric_name}-metric"), f"Метрика {metric_name}"
            )
            return metric_element.is_displayed()
        except:
            return False

    def get_metric_value(self, metric_name: str) -> str:
        """Возвращает значение метрики."""
        try:
            metric_element = self._find_element(
                (By.ID, f"{metric_name}-metric"), f"Метрика {metric_name}"
            )
            return metric_element.text
        except:
            return ""

    def wait_for_data_update(self, timeout: int = 30):
        """Ожидает обновления данных."""
        self.logger.info("Ожидаем обновления данных")
        import time

        time.sleep(timeout)

    def get_chart_data(self, chart_id: str) -> dict:
        """Возвращает данные графика."""
        try:
            chart_element = self._find_element((By.ID, chart_id), f"График {chart_id}")
            # Здесь можно добавить логику для извлечения данных из графика
            return {"labels": [], "data": []}
        except:
            return {"labels": [], "data": []}
