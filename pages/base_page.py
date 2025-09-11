from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, browser, url):
        self.browser = browser
        self.url = url

    def open(self):
        self.browser.get(self.url)

    def is_element_present(self, by_how, selector):
        try:
            self.browser.find_element(by_how, selector)
            return True
        except NoSuchElementException:
            return False

    def find_element(self, by_how, selector):
        return self.browser.find_element(by_how, selector)

    def wait_until_visible(self, locator):
        return WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located(locator))

    def wait_until_clickable(self, locator):
        return WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable(locator))

    def wait_until_not_visible(self, locator):
        return WebDriverWait(self.browser, 10).until(EC.invisibility_of_element_located(locator))

    def click_element_clickable(self, by_how, selector):
        element = self.wait_until_clickable((by_how, selector))
        element.click()

    def click_element_visible(self, by_how, selector):
        element = self.wait_until_visible((by_how, selector))
        element.click()

    def send_keys_to_element(self, by_how, selector, value):
        element = self.find_element(by_how, selector)
        element.send_keys(value)

    def scroll_to_element_and_click(self, by_how, selector):
        element = self.find_element(by_how, selector)
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        element.click()

    def scroll_to_element_and_send_keys(self, by_how, selector, value):
        element = self.find_element(by_how, selector)
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        element.send_keys(value)

