Это проект фреймворка автоматизации тестирование Е2Е, REST Api, DB (реляционные/не реляционные)
Для запуска тестов скачайте этот проект и выполните шаги ниже:
- python -m venv .venv - создать папку виртуального окружения для установки необходимых пакетов
- source .venv/bin/activate - переключится на виртуальную среду проекта
- pip install -r requirements.txt - установить все необходимые зависимости для работы проекта в виртуальном окружении
- pylint <file_or_folder_path> - проверка чистоты кода (не обязательно)
- pytest -m crit tests/ - запустить все Е2Е тесты
- pytest -m crit tests/test_login_page.py - запустить все Е2Е тесты из файла test_login_page.py
- pytest -m crit tests/test_login_page.py::test_sign_in - запустить тест test_sign_in из файла test_login_page.py