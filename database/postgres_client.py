import psycopg2
import allure

class PostgresClient:
    def __init__(self, db_host, db_port, db_user, db_password, db_name):
        """
        Инициализирует клиент для подключения к PostgreSQL.
        :param db_host: Хост базы данных.
        :param db_port: Порт базы данных.
        :param db_user: Имя пользователя.
        :param db_password: Пароль.
        :param db_name: Имя базы данных.
        """
        self.connection = psycopg2.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password,
            dbname=db_name
        )
        self.connection.autocommit = True

    @allure.step("Выполнение SQL-запроса: {query}")
    def execute_query(self, query, params=None, fetch=None):
        """
        Выполняет SQL-запрос.
        :param query: SQL-запрос.
        :param params: Параметры для запроса.
        :param fetch: 'one' для получения одной записи, 'all' для всех.
        :return: Результат запроса или None.
        """
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            if fetch == 'one':
                return cursor.fetchone()
            if fetch == 'all':
                return cursor.fetchall()
        return None

    @allure.step("Закрытие соединения с PostgreSQL")
    def close(self):
        """Закрывает соединение с базой данных."""
        if self.connection:
            self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
