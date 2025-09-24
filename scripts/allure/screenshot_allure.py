#!/usr/bin/env python3
"""
Скрипт для создания скриншота Allure отчета
"""

import os
import time
import requests
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


def wait_for_allure_server(allure_url, max_attempts=30):
    """Ожидание готовности Allure сервера"""
    print(f"⏳ Ожидание готовности Allure сервера {allure_url}...")
    
    for attempt in range(max_attempts):
        try:
            # Проверяем доступность главной страницы
            response = requests.get(allure_url, timeout=5)
            if response.status_code == 200:
                print("✅ Allure сервер готов")
                return True
        except:
            pass
        
        print(f"Попытка {attempt + 1}/{max_attempts}...")
        time.sleep(2)
    
    print("❌ Allure сервер не отвечает")
    return False


def take_allure_screenshot(allure_url, output_file):
    """Создание скриншота Allure отчета"""
    driver = setup_chrome_driver()
    if not driver:
        return False
    
    try:
        # URL отчета
        report_url = f"{allure_url}/allure-docker-service/projects/default/reports/latest/index.html"
        print(f"📊 Открытие Allure отчета: {report_url}")
        
        # Загрузка страницы
        driver.get(report_url)
        
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
    allure_url = os.getenv('ALLURE_URL', 'http://localhost:5050')
    allure_reports_dir = os.getenv('ALLURE_REPORTS_DIR', 'allure-reports/latest')
    
    # Создание папки для скриншотов
    screenshots_dir = Path(allure_reports_dir) / "screenshots"
    screenshots_dir.mkdir(exist_ok=True)
    
    # Проверка готовности Allure сервера
    if not wait_for_allure_server(allure_url):
        print("❌ Не удалось подключиться к Allure серверу")
        return 1
    
    # Создание скриншота
    screenshot_file = screenshots_dir / "allure_report_screenshot.png"
    success = take_allure_screenshot(allure_url, screenshot_file)
    
    if success:
        print(f"✅ Скриншот Allure отчета создан: {screenshot_file}")
        return 0
    else:
        print("❌ Ошибка создания скриншота")
        return 1


if __name__ == "__main__":
    exit(main())
