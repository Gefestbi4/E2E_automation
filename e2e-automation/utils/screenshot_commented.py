"""
Screenshot manager for E2E automation tests  # Документация менеджера скриншотов для E2E автоматизации
"""

import os  # Импорт модуля для работы с операционной системой
from datetime import datetime  # Импорт класса datetime для работы с датой и временем
from pathlib import Path  # Импорт Path для работы с путями файлов
from typing import Optional  # Импорт типа Optional для аннотаций типов
from selenium.webdriver.remote.webdriver import WebDriver  # Импорт класса WebDriver
from utils.logger import TestLogger  # Импорт класса TestLogger


class ScreenshotManager:  # Определение класса менеджера скриншотов
    """Manager for taking and organizing screenshots during tests"""  # Документация класса

    def __init__(self):  # Конструктор класса ScreenshotManager
        self.logger = TestLogger(
            "ScreenshotManager"
        )  # Инициализация логгера для менеджера скриншотов
        self.screenshots_dir = Path(
            "/app/screenshots"
        )  # Создание пути к папке скриншотов
        self.screenshots_dir.mkdir(
            exist_ok=True
        )  # Создание папки скриншотов если она не существует

        # Create subdirectories  # Комментарий о создании подпапок
        self.failure_dir = (
            self.screenshots_dir / "failures"
        )  # Создание пути к папке скриншотов падений
        self.success_dir = (
            self.screenshots_dir / "success"
        )  # Создание пути к папке скриншотов успехов
        self.step_dir = (
            self.screenshots_dir / "steps"
        )  # Создание пути к папке скриншотов шагов

        for directory in [
            self.failure_dir,
            self.success_dir,
            self.step_dir,
        ]:  # Цикл по всем подпапкам
            directory.mkdir(
                exist_ok=True
            )  # Создание каждой подпапки если она не существует

    def take_screenshot(  # Метод создания скриншота
        self, driver: WebDriver, name: str = "screenshot", category: str = "step"
    ) -> str:
        """
        Take screenshot and save to appropriate directory  # Документация метода

        Args:  # Аргументы метода
            driver: WebDriver instance  # Экземпляр WebDriver
            name: Screenshot name  # Имя скриншота
            category: Category (failure, success, step)  # Категория скриншота

        Returns:  # Возвращаемое значение
            Path to saved screenshot  # Путь к сохраненному скриншоту
        """
        try:  # Начало блока обработки исключений
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[
                :-3
            ]  # Создание временной метки
            filename = f"{name}_{timestamp}.png"  # Создание имени файла скриншота

            # Select directory based on category  # Комментарий о выборе папки по категории
            if category == "failure":  # Проверка категории - падение
                directory = self.failure_dir  # Установка папки для падений
            elif category == "success":  # Проверка категории - успех
                directory = self.success_dir  # Установка папки для успехов
            else:  # Иначе
                directory = self.step_dir  # Установка папки для шагов

            screenshot_path = directory / filename  # Создание полного пути к скриншоту

            # Take screenshot  # Комментарий о создании скриншота
            driver.save_screenshot(str(screenshot_path))  # Сохранение скриншота

            self.logger.screenshot(
                str(screenshot_path)
            )  # Логирование создания скриншота
            return str(screenshot_path)  # Возврат пути к скриншоту

        except Exception as e:  # Обработка исключений
            self.logger.error(
                f"Failed to take screenshot: {str(e)}"
            )  # Логирование ошибки создания скриншота
            raise  # Повторное возбуждение исключения

    def take_element_screenshot(  # Метод создания скриншота элемента
        self, driver: WebDriver, element, name: str = "element_screenshot"
    ) -> str:
        """
        Take screenshot of specific element  # Документация метода

        Args:  # Аргументы метода
            driver: WebDriver instance  # Экземпляр WebDriver
            element: WebElement to screenshot  # Веб-элемент для скриншота
            name: Screenshot name  # Имя скриншота

        Returns:  # Возвращаемое значение
            Path to saved screenshot  # Путь к сохраненному скриншоту
        """
        try:  # Начало блока обработки исключений
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[
                :-3
            ]  # Создание временной метки
            filename = f"{name}_{timestamp}.png"  # Создание имени файла скриншота
            screenshot_path = self.step_dir / filename  # Создание пути к скриншоту

            # Take element screenshot  # Комментарий о создании скриншота элемента
            element.screenshot(str(screenshot_path))  # Сохранение скриншота элемента

            self.logger.screenshot(
                str(screenshot_path)
            )  # Логирование создания скриншота
            return str(screenshot_path)  # Возврат пути к скриншоту

        except Exception as e:  # Обработка исключений
            self.logger.error(
                f"Failed to take element screenshot: {str(e)}"
            )  # Логирование ошибки создания скриншота элемента
            raise  # Повторное возбуждение исключения

    def take_full_page_screenshot(  # Метод создания скриншота всей страницы
        self, driver: WebDriver, name: str = "full_page_screenshot"
    ) -> str:
        """
        Take full page screenshot (including scrolled content)  # Документация метода

        Args:  # Аргументы метода
            driver: WebDriver instance  # Экземпляр WebDriver
            name: Screenshot name  # Имя скриншота

        Returns:  # Возвращаемое значение
            Path to saved screenshot  # Путь к сохраненному скриншоту
        """
        try:  # Начало блока обработки исключений
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[
                :-3
            ]  # Создание временной метки
            filename = f"{name}_{timestamp}.png"  # Создание имени файла скриншота
            screenshot_path = self.step_dir / filename  # Создание пути к скриншоту

            # Get page dimensions  # Комментарий о получении размеров страницы
            total_width = driver.execute_script(
                "return document.body.scrollWidth"
            )  # Получение полной ширины страницы
            total_height = driver.execute_script(
                "return document.body.scrollHeight"
            )  # Получение полной высоты страницы

            # Set window size to full page  # Комментарий об установке размера окна на всю страницу
            driver.set_window_size(
                total_width, total_height
            )  # Установка размера окна на размеры страницы

            # Take screenshot  # Комментарий о создании скриншота
            driver.save_screenshot(str(screenshot_path))  # Сохранение скриншота

            # Restore original window size  # Комментарий о восстановлении оригинального размера окна
            driver.set_window_size(
                1920, 1080
            )  # Восстановление стандартного размера окна

            self.logger.screenshot(
                str(screenshot_path)
            )  # Логирование создания скриншота
            return str(screenshot_path)  # Возврат пути к скриншоту

        except Exception as e:  # Обработка исключений
            self.logger.error(
                f"Failed to take full page screenshot: {str(e)}"
            )  # Логирование ошибки создания скриншота всей страницы
            raise  # Повторное возбуждение исключения

    def cleanup_old_screenshots(self, days: int = 7):  # Метод очистки старых скриншотов
        """
        Clean up screenshots older than specified days  # Документация метода

        Args:  # Аргументы метода
            days: Number of days to keep screenshots  # Количество дней для хранения скриншотов
        """
        try:  # Начало блока обработки исключений
            cutoff_time = datetime.now().timestamp() - (
                days * 24 * 60 * 60
            )  # Вычисление времени отсечения

            for directory in [
                self.failure_dir,
                self.success_dir,
                self.step_dir,
            ]:  # Цикл по всем папкам скриншотов
                for file_path in directory.iterdir():  # Цикл по всем файлам в папке
                    if (
                        file_path.is_file() and file_path.stat().st_mtime < cutoff_time
                    ):  # Проверка что файл старый
                        file_path.unlink()  # Удаление старого файла
                        self.logger.debug(
                            f"Deleted old screenshot: {file_path}"
                        )  # Логирование удаления старого скриншота

        except Exception as e:  # Обработка исключений
            self.logger.error(
                f"Failed to cleanup old screenshots: {str(e)}"
            )  # Логирование ошибки очистки старых скриншотов

    def get_screenshot_count(
        self, category: str = "all"
    ) -> dict:  # Метод получения количества скриншотов
        """
        Get count of screenshots by category  # Документация метода

        Args:  # Аргументы метода
            category: Category to count (all, failure, success, step)  # Категория для подсчета

        Returns:  # Возвращаемое значение
            Dictionary with screenshot counts  # Словарь с количеством скриншотов
        """
        try:  # Начало блока обработки исключений
            counts = {}  # Инициализация словаря счетчиков

            if category == "all" or category == "failure":  # Проверка категории падений
                counts["failure"] = len(
                    list(self.failure_dir.glob("*.png"))
                )  # Подсчет скриншотов падений

            if category == "all" or category == "success":  # Проверка категории успехов
                counts["success"] = len(
                    list(self.success_dir.glob("*.png"))
                )  # Подсчет скриншотов успехов

            if category == "all" or category == "step":  # Проверка категории шагов
                counts["step"] = len(
                    list(self.step_dir.glob("*.png"))
                )  # Подсчет скриншотов шагов

            if category == "all":  # Проверка категории все
                counts["total"] = sum(
                    counts.values()
                )  # Подсчет общего количества скриншотов

            return counts  # Возврат словаря счетчиков

        except Exception as e:  # Обработка исключений
            self.logger.error(
                f"Failed to get screenshot count: {str(e)}"
            )  # Логирование ошибки получения количества скриншотов
            return {}  # Возврат пустого словаря

    def get_latest_screenshot(
        self, category: str = "step"
    ) -> Optional[str]:  # Метод получения последнего скриншота
        """
        Get path to latest screenshot in category  # Документация метода

        Args:  # Аргументы метода
            category: Category to search (failure, success, step)  # Категория для поиска

        Returns:  # Возвращаемое значение
            Path to latest screenshot or None  # Путь к последнему скриншоту или None
        """
        try:  # Начало блока обработки исключений
            if category == "failure":  # Проверка категории падений
                directory = self.failure_dir  # Установка папки падений
            elif category == "success":  # Проверка категории успехов
                directory = self.success_dir  # Установка папки успехов
            else:  # Иначе
                directory = self.step_dir  # Установка папки шагов

            png_files = list(directory.glob("*.png"))  # Получение списка PNG файлов
            if png_files:  # Проверка наличия файлов
                latest_file = max(
                    png_files, key=lambda x: x.stat().st_mtime
                )  # Поиск самого нового файла
                return str(latest_file)  # Возврат пути к самому новому файлу

            return None  # Возврат None если файлы не найдены

        except Exception as e:  # Обработка исключений
            self.logger.error(
                f"Failed to get latest screenshot: {str(e)}"
            )  # Логирование ошибки получения последнего скриншота
            return None  # Возврат None при ошибке

    def create_screenshot_report(self) -> str:  # Метод создания отчета по скриншотам
        """
        Create HTML report of all screenshots  # Документация метода

        Returns:  # Возвращаемое значение
            Path to HTML report  # Путь к HTML отчету
        """
        try:  # Начало блока обработки исключений
            report_path = (
                self.screenshots_dir / "screenshot_report.html"
            )  # Создание пути к HTML отчету

            html_content = """  # Начало HTML контента
            <!DOCTYPE html>
            <html>
            <head>
                <title>Screenshot Report</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 20px; }
                    .category { margin-bottom: 30px; }
                    .category h2 { color: #333; border-bottom: 2px solid #ccc; }
                    .screenshot { margin: 10px 0; }
                    .screenshot img { max-width: 800px; border: 1px solid #ddd; }
                    .screenshot p { margin: 5px 0; font-size: 12px; color: #666; }
                </style>
            </head>
            <body>
                <h1>Screenshot Report</h1>
                <p>Generated: {timestamp}</p>
            """.format(  # Форматирование HTML с временной меткой
                timestamp=datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )  # Вставка текущего времени
            )

            # Add screenshots by category  # Комментарий о добавлении скриншотов по категориям
            for category, directory in [  # Цикл по категориям и папкам
                ("Failures", self.failure_dir),  # Категория падений
                ("Success", self.success_dir),  # Категория успехов
                ("Steps", self.step_dir),  # Категория шагов
            ]:
                html_content += f'<div class="category"><h2>{category}</h2>'  # Добавление заголовка категории

                png_files = sorted(  # Сортировка PNG файлов
                    directory.glob("*.png"),  # Поиск всех PNG файлов в папке
                    key=lambda x: x.stat().st_mtime,  # Сортировка по времени модификации
                    reverse=True,  # В обратном порядке (новые сначала)
                )

                for file_path in png_files:  # Цикл по PNG файлам
                    relative_path = file_path.relative_to(
                        self.screenshots_dir
                    )  # Получение относительного пути
                    file_time = datetime.fromtimestamp(
                        file_path.stat().st_mtime
                    )  # Получение времени файла

                    html_content += f"""  # Добавление HTML для скриншота
                    <div class="screenshot">
                        <img src="{relative_path}" alt="{file_path.name}">
                        <p>{file_path.name} - {file_time.strftime("%Y-%m-%d %H:%M:%S")}</p>
                    </div>
                    """

                html_content += "</div>"  # Закрытие div категории

            html_content += "</body></html>"  # Завершение HTML

            with open(
                report_path, "w", encoding="utf-8"
            ) as f:  # Открытие файла для записи
                f.write(html_content)  # Запись HTML контента в файл

            self.logger.info(
                f"Screenshot report created: {report_path}"
            )  # Логирование создания отчета
            return str(report_path)  # Возврат пути к отчету

        except Exception as e:  # Обработка исключений
            self.logger.error(
                f"Failed to create screenshot report: {str(e)}"
            )  # Логирование ошибки создания отчета
            raise  # Повторное возбуждение исключения
