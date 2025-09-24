#!/bin/bash

# Скрипт для очистки временных файлов

echo "🧹 Очистка временных файлов..."
echo "================================"

# Создание backup директории
mkdir -p backup_scripts

echo "📦 Создание backup временных скриптов..."
mv demo_e2e.sh backup_scripts/ 2>/dev/null || echo "demo_e2e.sh не найден"
mv demo_local.sh backup_scripts/ 2>/dev/null || echo "demo_local.sh не найден"
mv test_telegram.py backup_scripts/ 2>/dev/null || echo "test_telegram.py не найден"

echo "✅ Временные скрипты перемещены в backup_scripts/"
echo ""
echo "📁 Оставшиеся основные скрипты:"
echo "- scripts/send_allure_report.py (основной для Telegram)"
echo "- scripts/run_e2e_tests.sh (основной для Docker)"
echo "- run_e2e_tests.sh (основной для запуска системы)"
echo ""
echo "🔄 Для восстановления временных скриптов:"
echo "mv backup_scripts/* ."
