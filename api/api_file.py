from api_client import ApiClient
import allure

class FileApi(ApiClient):
    def upload_file(self, file_path):
        """
        Загружает файл на сервер.
        :param file_path: Путь к файлу.
        :return: Ответ сервера в формате JSON.
        """
        with open(file_path, 'rb') as f:
            files = {'file': f}
            return self.post('/upload', files=files)

    def get_file_url(self, file_id):
        """
        Получает URL файла по ID.
        :param file_id: ID файла.
        :return: URL файла.
        """
        return self.get(f'/file/{file_id}')['url']

    def delete_file(self, file_id):
        """
        Удаляет файл по ID.
        :param file_id: ID файла.
        """
        return self.delete(f'/file/{file_id}')

    def download_file(self, file_id):
        """
        Скачивает файл по ID.
        :param file_id: ID файла.
        :return: Содержимое файла в байтах.
        """
        file_url = self.get_file_url(file_id)
        with allure.step(f"Скачивание файла по URL: {file_url}"):
            response = self.session.get(file_url)
            response.raise_for_status()
            allure.attach(response.content, 'Downloaded File', allure.attachment_type.DEFAULT)
            return response.content