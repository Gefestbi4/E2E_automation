# 🛠️ Scripts

Общие скрипты для автоматизации, отчетности и уведомлений.

## 📁 Структура
```
scripts/
├── telegram/           # Telegram интеграция
│   ├── send_final_report.py
│   └── test_telegram.py
├── allure/            # Allure отчеты
│   ├── screenshot_allure.py
│   ├── screenshot_local_allure.py
│   └── open_allure_report.sh
├── requirements.txt   # Зависимости
├── .env              # Переменные окружения
└── README.md         # Документация
```

## 🚀 Использование

### Telegram уведомления
```bash
# Тест подключения к Telegram
python3 telegram/test_telegram.py

# Отправка отчета
python3 telegram/send_final_report.py
```

### Allure отчеты
```bash
# Создание скриншота
python3 allure/screenshot_allure.py

# Открытие отчета
./allure/open_allure_report.sh
```

## 🔧 Конфигурация

Основные переменные в `.env`:
- `TELEGRAM_BOT_TOKEN` - Токен Telegram бота
- `TELEGRAM_CHAT_ID` - ID чата для уведомлений
- `ALLURE_RESULTS_DIR` - Директория результатов Allure
- `ALLURE_REPORTS_DIR` - Директория отчетов Allure