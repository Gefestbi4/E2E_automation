"""
Система маркировки тестов для отладки
"""

import pytest
import os
from typing import List, Set


class TestMarkers:
    """Класс для управления маркерами тестов"""

    DEBUG_MARKERS = {"debug", "fixme"}
    PRIORITY_MARKERS = {"critical", "high", "medium", "low"}
    TYPE_MARKERS = {
        "smoke",
        "regression",
        "api",
        "ui",
        "database",
        "performance",
        "security",
    }
    MODULE_MARKERS = {"auth", "ecommerce", "social", "tasks", "content", "analytics"}

    @classmethod
    def get_debug_tests(cls) -> List[str]:
        """Получить список тестов для отладки"""
        return cls._get_tests_by_markers(cls.DEBUG_MARKERS)

    @classmethod
    def mark_test_for_debug(cls, test_name: str, reason: str = ""):
        """Пометить тест для отладки"""
        cls._add_marker_to_test(test_name, "debug", reason)

    @classmethod
    def mark_test_as_broken(cls, test_name: str, reason: str = ""):
        """Пометить тест как сломанный"""
        cls._add_marker_to_test(test_name, "fixme", reason)

    @classmethod
    def remove_debug_marker(cls, test_name: str):
        """Убрать маркер отладки с теста"""
        cls._remove_marker_from_test(test_name, cls.DEBUG_MARKERS)

    @classmethod
    def get_tests_by_priority(cls, priority: str) -> List[str]:
        """Получить тесты по приоритету"""
        if priority not in cls.PRIORITY_MARKERS:
            raise ValueError(f"Invalid priority: {priority}")
        return cls._get_tests_by_markers({priority})

    @classmethod
    def get_tests_by_type(cls, test_type: str) -> List[str]:
        """Получить тесты по типу"""
        if test_type not in cls.TYPE_MARKERS:
            raise ValueError(f"Invalid test type: {test_type}")
        return cls._get_tests_by_markers({test_type})

    @classmethod
    def get_tests_by_module(cls, module: str) -> List[str]:
        """Получить тесты по модулю"""
        if module not in cls.MODULE_MARKERS:
            raise ValueError(f"Invalid module: {module}")
        return cls._get_tests_by_markers({module})

    @classmethod
    def _get_tests_by_markers(cls, markers: Set[str]) -> List[str]:
        """Получить тесты по маркерам"""
        # Здесь должна быть логика поиска тестов с указанными маркерами
        # В реальной реализации это может быть парсинг файлов тестов
        return []

    @classmethod
    def _add_marker_to_test(cls, test_name: str, marker: str, reason: str = ""):
        """Добавить маркер к тесту"""
        # Здесь должна быть логика добавления маркера к тесту
        # В реальной реализации это может быть модификация файла теста
        pass

    @classmethod
    def _remove_marker_from_test(cls, test_name: str, markers: Set[str]):
        """Убрать маркеры с теста"""
        # Здесь должна быть логика удаления маркеров с теста
        pass


def pytest_collection_modifyitems(config, items):
    """Модификация коллекции тестов"""

    # Получаем маркеры из командной строки
    debug_only = config.getoption("--debug-only", default=False)
    fixme_only = config.getoption("--fixme-only", default=False)

    if debug_only:
        # Запускаем только тесты с маркером debug
        selected_items = [item for item in items if item.get_closest_marker("debug")]
        items[:] = selected_items
        print(f"🔍 Запуск только тестов для отладки: {len(selected_items)} тестов")

    if fixme_only:
        # Запускаем только тесты с маркером fixme
        selected_items = [item for item in items if item.get_closest_marker("fixme")]
        items[:] = selected_items
        print(f"🔧 Запуск только сломанных тестов: {len(selected_items)} тестов")

    # Добавляем информацию о маркерах в отчет
    for item in items:
        markers = [marker.name for marker in item.iter_markers()]
        if "debug" in markers:
            print(f"🐛 Тест {item.name} помечен для отладки")
        if "fixme" in markers:
            print(f"⚠️  Тест {item.name} помечен как сломанный")


def pytest_addoption(parser):
    """Добавление опций командной строки"""
    parser.addoption(
        "--debug-only",
        action="store_true",
        default=False,
        help="Запустить только тесты с маркером debug",
    )
    parser.addoption(
        "--fixme-only",
        action="store_true",
        default=False,
        help="Запустить только тесты с маркером fixme",
    )
    parser.addoption(
        "--mark-fixed",
        action="store_true",
        default=False,
        help="Автоматически убрать маркер debug с пройденных тестов",
    )


def pytest_runtest_logreport(report):
    """Обработка результатов тестов"""
    if report.when == "call" and report.outcome == "passed":
        # Если тест прошел и есть опция --mark-fixed
        if hasattr(report, "node") and report.node.get_closest_marker("debug"):
            print(f"✅ Тест {report.node.name} прошел! Можно убрать маркер debug")


# Декораторы для маркировки тестов
def debug_test(reason: str = ""):
    """Декоратор для маркировки теста как требующего отладки"""
    return pytest.mark.debug(reason=reason)


def fixme_test(reason: str = ""):
    """Декоратор для маркировки теста как сломанного"""
    return pytest.mark.fixme(reason=reason)


def critical_test(reason: str = ""):
    """Декоратор для маркировки критического теста"""
    return pytest.mark.critical(reason=reason)


def high_priority(reason: str = ""):
    """Декоратор для маркировки теста высокого приоритета"""
    return pytest.mark.high(reason=reason)


def medium_priority(reason: str = ""):
    """Декоратор для маркировки теста среднего приоритета"""
    return pytest.mark.medium(reason=reason)


def low_priority(reason: str = ""):
    """Декоратор для маркировки теста низкого приоритета"""
    return pytest.mark.low(reason=reason)


def smoke_test(reason: str = ""):
    """Декоратор для маркировки smoke теста"""
    return pytest.mark.smoke(reason=reason)


def regression_test(reason: str = ""):
    """Декоратор для маркировки регрессионного теста"""
    return pytest.mark.regression(reason=reason)


# Утилиты для работы с маркерами
def get_marked_tests(marker_name: str) -> List[str]:
    """Получить список тестов с определенным маркером"""
    # В реальной реализации здесь может быть парсинг файлов тестов
    return []


def print_test_summary():
    """Вывести сводку по маркированным тестам"""
    print("\n📊 Сводка по маркированным тестам:")

    debug_tests = TestMarkers.get_debug_tests()
    if debug_tests:
        print(f"🐛 Тесты для отладки: {len(debug_tests)}")
        for test in debug_tests:
            print(f"   - {test}")

    print(f"🎯 Критические тесты: {len(TestMarkers.get_tests_by_priority('critical'))}")
    print(f"🔥 Высокий приоритет: {len(TestMarkers.get_tests_by_priority('high'))}")
    print(f"📊 Средний приоритет: {len(TestMarkers.get_tests_by_priority('medium'))}")
    print(f"📝 Низкий приоритет: {len(TestMarkers.get_tests_by_priority('low'))}")

    print(f"💨 Smoke тесты: {len(TestMarkers.get_tests_by_type('smoke'))}")
    print(f"🔄 Регрессионные тесты: {len(TestMarkers.get_tests_by_type('regression'))}")


if __name__ == "__main__":
    print_test_summary()
