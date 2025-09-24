#!/usr/bin/env python3
"""
Скрипт для создания скриншота локального Allure отчета
"""

import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path


def setup_chrome_driver():
    """Настройка Chrome WebDriver для скриншотов"""
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')  # Большой размер для полного отчета
    chrome_options.add_argument('--disable-web-security')
    chrome_options.add_argument('--allow-running-insecure-content')
    chrome_options.add_argument('--force-device-scale-factor=1')
    chrome_options.add_argument('--high-dpi-support=1')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-plugins')
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver
    except Exception as e:
        print(f"Ошибка настройки Chrome WebDriver: {e}")
        return None


def take_local_allure_screenshot(allure_reports_dir, output_file):
    """Создание скриншота локального Allure отчета"""
    driver = setup_chrome_driver()
    if not driver:
        return False
    
    try:
        # Путь к локальному HTML файлу
        index_file = Path(allure_reports_dir) / "index.html"
        if not index_file.exists():
            print(f"❌ Файл index.html не найден: {index_file}")
            return False
        
        # URL локального файла
        file_url = f"file://{index_file.absolute()}"
        print(f"📊 Открытие локального Allure отчета: {file_url}")
        
        # Загрузка страницы
        driver.get(file_url)
        
        # Ожидание загрузки страницы
        time.sleep(10)
        
        # Прокрутка в начало страницы
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(2)
        
        # Создание скриншота
        driver.save_screenshot(output_file)
        print(f"📸 Скриншот сохранен: {output_file}")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка создания скриншота: {e}")
        return False
    finally:
        driver.quit()


def main():
    """Основная функция"""
    allure_reports_dir = os.getenv('ALLURE_REPORTS_DIR', 'allure-reports/latest')
    
    # Создание папки для скриншотов
    screenshots_dir = Path(allure_reports_dir) / "screenshots"
    screenshots_dir.mkdir(exist_ok=True)
    
    # Создание скриншота
    screenshot_file = screenshots_dir / "allure_report_screenshot.png"
    success = take_local_allure_screenshot(allure_reports_dir, screenshot_file)
    
    if success:
        print(f"✅ Скриншот локального Allure отчета создан: {screenshot_file}")
        return 0
    else:
        print("❌ Ошибка создания скриншота")
        return 1


if __name__ == "__main__":
    exit(main())
