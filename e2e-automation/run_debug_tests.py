#!/usr/bin/env python3
"""
Скрипт для запуска тестов с маркировкой отладки
"""
import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description):
    """Выполнение команды с выводом результата"""
    print(f"\n🔧 {description}")
    print(f"Команда: {command}")
    print("-" * 50)

    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        if result.stdout:
            print("STDOUT:")
            print(result.stdout)

        if result.stderr:
            print("STDERR:")
            print(result.stderr)

        print(f"Код возврата: {result.returncode}")
        return result.returncode == 0

    except Exception as e:
        print(f"Ошибка выполнения команды: {e}")
        return False


def main():
    """Основная функция"""
    print("🧪 Запуск тестов с системой маркировки")
    print("=" * 60)

    # Проверяем, что мы в правильной директории
    if not os.path.exists("pytest.ini"):
        print(
            "❌ Ошибка: pytest.ini не найден. Запустите скрипт из директории e2e-automation"
        )
        sys.exit(1)

    # Меню выбора
    print("\nВыберите тип запуска тестов:")
    print("1. Только тесты для отладки (--debug-only)")
    print("2. Только сломанные тесты (--fixme-only)")
    print("3. Критические тесты")
    print("4. Тесты высокого приоритета")
    print("5. Smoke тесты")
    print("6. Все тесты")
    print("7. Конкретный тест")
    print("8. Тесты модуля")

    choice = input("\nВведите номер (1-8): ").strip()

    commands = {
        "1": {
            "cmd": "pytest --debug-only -v --tb=short",
            "desc": "Запуск только тестов для отладки",
        },
        "2": {
            "cmd": "pytest --fixme-only -v --tb=short",
            "desc": "Запуск только сломанных тестов",
        },
        "3": {
            "cmd": "pytest -m critical -v --tb=short",
            "desc": "Запуск критических тестов",
        },
        "4": {
            "cmd": "pytest -m high -v --tb=short",
            "desc": "Запуск тестов высокого приоритета",
        },
        "5": {"cmd": "pytest -m smoke -v --tb=short", "desc": "Запуск smoke тестов"},
        "6": {"cmd": "pytest -v --tb=short", "desc": "Запуск всех тестов"},
        "7": {"cmd": "", "desc": "Запуск конкретного теста"},
        "8": {"cmd": "", "desc": "Запуск тестов модуля"},
    }

    if choice in commands:
        if choice == "7":
            test_path = input(
                "Введите путь к тесту (например: tests/test_auth.py::TestLogin::test_successful_login): "
            )
            commands[choice]["cmd"] = f"pytest {test_path} -v --tb=short"

        elif choice == "8":
            print("\nДоступные модули:")
            print("- auth (Аутентификация)")
            print("- ecommerce (E-commerce)")
            print("- social (Социальная сеть)")
            print("- tasks (Управление задачами)")
            print("- content (Управление контентом)")
            print("- analytics (Аналитика)")

            module = input("Введите название модуля: ").strip().lower()
            commands[choice]["cmd"] = f"pytest -m {module} -v --tb=short"

        # Выполняем команду
        success = run_command(commands[choice]["cmd"], commands[choice]["desc"])

        if success:
            print("\n✅ Тесты выполнены успешно")

            # Предлагаем убрать маркеры debug с прошедших тестов
            if choice in ["1", "2"]:
                remove_markers = (
                    input("\nУбрать маркеры debug с прошедших тестов? (y/n): ")
                    .strip()
                    .lower()
                )
                if remove_markers == "y":
                    print("\n🔧 Удаление маркеров debug с прошедших тестов...")
                    # Здесь должна быть логика удаления маркеров
                    print("Функция удаления маркеров будет реализована")
        else:
            print("\n❌ Тесты завершились с ошибками")

    else:
        print("❌ Неверный выбор")
        sys.exit(1)


def show_test_summary():
    """Показать сводку по тестам"""
    print("\n📊 Сводка по маркированным тестам:")
    print("-" * 40)

    # Здесь должна быть логика подсчета тестов по маркерам
    summary = {
        "debug": "Найдено X тестов для отладки",
        "fixme": "Найдено X сломанных тестов",
        "critical": "Найдено X критических тестов",
        "high": "Найдено X тестов высокого приоритета",
        "smoke": "Найдено X smoke тестов",
    }

    for marker, description in summary.items():
        print(f"  {description}")


def cleanup_markers():
    """Очистка маркеров debug с прошедших тестов"""
    print("\n🧹 Очистка маркеров debug...")
    # Здесь должна быть логика очистки маркеров
    print("Функция очистки маркеров будет реализована")


if __name__ == "__main__":
    try:
        if len(sys.argv) > 1 and sys.argv[1] == "--summary":
            show_test_summary()
        elif len(sys.argv) > 1 and sys.argv[1] == "--cleanup":
            cleanup_markers()
        else:
            main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Выполнение прервано пользователем")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        sys.exit(1)
