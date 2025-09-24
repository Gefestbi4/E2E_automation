# 📊 Доступ к Allure отчетам

## 🎯 **Проблема**
По умолчанию по адресу `http://localhost:5050` открывается Swagger UI документация, а не сам отчет.

## ✅ **Решение**

### **1. Прямой доступ к отчету:**
```
http://localhost:5050/allure-docker-service/projects/default/reports/latest/index.html
```

### **2. Через скрипт (рекомендуется):**
```bash
# Открыть отчет в браузере
./run_tests.sh report

# Или напрямую
./scripts/open_allure_report.sh
```

### **3. Через главный скрипт:**
```bash
# Все доступные режимы
./run_tests.sh [local|docker|demo|report]

# Открыть только отчет
./run_tests.sh report
```

## 🔧 **Настройка**

### **Автоматическое открытие:**
Скрипт автоматически определяет операционную систему и открывает браузер:
- **macOS**: `open`
- **Linux**: `xdg-open`
- **Windows**: `start`

### **Ручное открытие:**
Если автоматическое открытие не работает, скопируйте URL:
```
http://localhost:5050/allure-docker-service/projects/default/reports/latest/index.html
```

## 📋 **Проверка статуса**

### **Проверить, что Allure сервер запущен:**
```bash
curl http://localhost:5050/allure-docker-service/version
```

### **Проверить статус контейнера:**
```bash
docker compose ps allure
```

### **Перезапустить Allure сервер:**
```bash
docker compose restart allure
```

## 🎯 **Доступные отчеты**

### **Последний отчет:**
- URL: `http://localhost:5050/allure-docker-service/projects/default/reports/latest/index.html`
- Описание: Самый свежий сгенерированный отчет

### **Все отчеты:**
- URL: `http://localhost:5050/allure-docker-service/projects/default/reports/`
- Описание: Список всех доступных отчетов

### **API документация:**
- URL: `http://localhost:5050/allure-docker-service/swagger/`
- Описание: Swagger UI для API

## 🚀 **Быстрый старт**

```bash
# 1. Запустить тесты
./run_tests.sh local

# 2. Открыть отчет
./run_tests.sh report
```

## 📱 **Интеграция с Telegram**

Отчеты также автоматически отправляются в Telegram:
- ✅ **ZIP архив** с полным отчетом
- ✅ **Статистика** тестов
- ✅ **Время выполнения**
- ✅ **Статус** каждого теста

## 🎉 **Готово!**

Теперь у вас есть удобный доступ к Allure отчетам через простые команды!
