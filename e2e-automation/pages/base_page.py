
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, browser, url):
        """
        Конструктор класса BasePage.
        :param browser: Экземпляр WebDriver.
        :param url: URL-адрес страницы.
        """
        self.browser = browser
        self.url = url

    def open(self):
        """Открывает URL страницы в браузере."""
        self.browser.get(self.url)

    def is_element_present(self, by_how, selector):
        """
        Проверяет наличие элемента на странице.
        :param by_how: Метод поиска (например, By.ID).
        :param selector: Селектор элемента.
        :return: True, если элемент найден, иначе False.
        """
        try:
            self.browser.find_element(by_how, selector)
            return True
        except NoSuchElementException:
            return False

    def find_element(self, by_how, selector):
        """
        Находит один элемент на странице.
        :param by_how: Метод поиска.
        :param selector: Селектор элемента.
        :return: Найденный WebElement.
        """
        return self.browser.find_element(by_how, selector)

    def wait_until_visible(self, locator):
        """
        Ожидает, пока элемент станет видимым.
        :param locator: Кортеж (by_how, selector).
        :return: WebElement, когда он становится видимым.
        """
        return WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located(locator))

    def wait_until_clickable(self, locator):
        """
        Ожидает, пока элемент станет кликабельным.
        :param locator: Кортеж (by_how, selector).
        :return: WebElement, когда он становится кликабельным.
        """
        return WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable(locator))

    def wait_until_not_visible(self, locator):
        """
        Ожидает, пока элемент исчезнет со страницы.
        :param locator: Кортеж (by_how, selector).
        :return: True, если элемент исчез, иначе TimeoutException.
        """
        return WebDriverWait(self.browser, 10).until(EC.invisibility_of_element_located(locator))

    def click_element_clickable(self, by_how, selector):
        """
        Ожидает, пока элемент станет кликабельным, и кликает по нему.
        :param by_how: Метод поиска.
        :param selector: Селектор элемента.
        """
        element = self.wait_until_clickable((by_how, selector))
        element.click()

    def click_element_visible(self, by_how, selector):
        """
        Ожидает, пока элемент станет видимым, и кликает по нему.
        :param by_how: Метод поиска.
        :param selector: Селектор элемента.
        """
        element = self.wait_until_visible((by_how, selector))
        element.click()

    def send_keys_to_element(self, by_how, selector, value):
        """
        Находит элемент и вводит в него текст.
        :param by_how: Метод поиска.
        :param selector: Селектор элемента.
        :param value: Текст для ввода.
        """
        element = self.find_element(by_how, selector)
        element.send_keys(value)

    def scroll_to_element_and_click(self, by_how, selector):
        """
        Прокручивает страницу до элемента и кликает по нему.
        :param by_how: Метод поиска.
        :param selector: Селектор элемента.
        """
        element = self.find_element(by_how, selector)
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        element.click()

    def scroll_to_element_and_send_keys(self, by_how, selector, value):
        """
        Прокручивает страницу до элемента и вводит в него текст.
        :param by_how: Метод поиска.
        :param selector: Селектор элемента.
        :param value: Текст для ввода.
        """
        element = self.find_element(by_how, selector)
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        element.send_keys(value)
    
    def wait_for_element_visible(self, by_how, selector, timeout=10):
        """
        Ожидает, пока элемент станет видимым.
        :param by_how: Метод поиска.
        :param selector: Селектор элемента.
        :param timeout: Время ожидания в секундах.
        :return: WebElement, когда он становится видимым.
        """
        return WebDriverWait(self.browser, timeout).until(EC.visibility_of_element_located((by_how, selector)))
    
    def wait_for_element_clickable(self, by_how, selector, timeout=10):
        """
        Ожидает, пока элемент станет кликабельным.
        :param by_how: Метод поиска.
        :param selector: Селектор элемента.
        :param timeout: Время ожидания в секундах.
        :return: WebElement, когда он становится кликабельным.
        """
        return WebDriverWait(self.browser, timeout).until(EC.element_to_be_clickable((by_how, selector)))
    
    def wait_for_element_present(self, by_how, selector, timeout=10):
        """
        Ожидает, пока элемент появится на странице.
        :param by_how: Метод поиска.
        :param selector: Селектор элемента.
        :param timeout: Время ожидания в секундах.
        :return: WebElement, когда он появляется.
        """
        return WebDriverWait(self.browser, timeout).until(EC.presence_of_element_located((by_how, selector)))
    
    def is_element_visible(self, by_how, selector):
        """
        Проверяет, видим ли элемент на странице.
        :param by_how: Метод поиска.
        :param selector: Селектор элемента.
        :return: True, если элемент видим, иначе False.
        """
        try:
            element = self.find_element(by_how, selector)
            return element.is_displayed()
        except NoSuchElementException:
            return False
    
    def is_element_enabled(self, by_how, selector):
        """
        Проверяет, активен ли элемент.
        :param by_how: Метод поиска.
        :param selector: Селектор элемента.
        :return: True, если элемент активен, иначе False.
        """
        try:
            element = self.find_element(by_how, selector)
            return element.is_enabled()
        except NoSuchElementException:
            return False
    
    def get_element_text(self, by_how, selector):
        """
        Получает текст элемента.
        :param by_how: Метод поиска.
        :param selector: Селектор элемента.
        :return: Текст элемента.
        """
        element = self.find_element(by_how, selector)
        return element.text
    
    def get_element_attribute(self, by_how, selector, attribute):
        """
        Получает атрибут элемента.
        :param by_how: Метод поиска.
        :param selector: Селектор элемента.
        :param attribute: Имя атрибута.
        :return: Значение атрибута.
        """
        element = self.find_element(by_how, selector)
        return element.get_attribute(attribute)
    
    def clear_element(self, by_how, selector):
        """
        Очищает поле ввода.
        :param by_how: Метод поиска.
        :param selector: Селектор элемента.
        """
        element = self.find_element(by_how, selector)
        element.clear()
    
    def wait_for_url_change(self, expected_url, timeout=10):
        """
        Ожидает изменения URL.
        :param expected_url: Ожидаемый URL.
        :param timeout: Время ожидания в секундах.
        :return: True, если URL изменился, иначе False.
        """
        try:
            WebDriverWait(self.browser, timeout).until(lambda driver: expected_url in driver.current_url)
            return True
        except:
            return False