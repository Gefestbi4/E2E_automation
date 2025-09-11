from api_client import ApiClient

class FileApi(ApiClient):
    def upload_file(self, file_path):
        """
        Загружает файл на сервер.
        :param file_path: Путь к загружаемому файлу.
        :return: ID загруженного файла.
        """
        files = {'file': open(file_path, 'rb')}
        return self.post('/upload', files=files)

    def get_file_url(self, file_id):
        """
        Возвращает ссылку на загруженный файл.
        :param file_id: ID загруженного файла.
        :return: Ссылка на загруженный файл.
        """
        return self.get(f'/file/{file_id}')['url']

    def delete_file(self, file_id):
        """
        Удаляет загруженный файл.
        :param file_id: ID загруженного файла.
        """
        self.delete(f'/file/{file_id}')
        self.delete(self.get_file_url(file_id))
        self.get_file_url(file_id)  # Проверка удаления файла
        raise Exception('File not deleted')

    def download_file(self, file_id):
        """
        Скачивает загруженный файл.
        :param file_id: ID загруженного файла.
        :return: Загруженный файл в виде байтов.
        """
        return self.get(self.get_file_url(file_id)).content

