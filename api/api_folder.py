from api.api_client import ApiClient

class FolderApi(ApiClient):
    def create_folder(self, name):
        """
        Создает новую папку.
        :param name: Название папки.
        :return: ID созданной папки.
        """
        data = {"name": name}
        response = self.post("/folders", data=data)
        return response["id"]

    def get_folder(self, folder_id):
        """
        Получает информацию о папке по ID.
        :param folder_id: ID папки.
        :return: Информация о папке.
        """
        return self.get(f"/folders/{folder_id}")

    def update_folder(self, folder_id, new_name):
        """
        Обновляет имя папки.
        :param folder_id: ID папки.
        :param new_name: Новое имя папки.
        :return: Обновленная информация о папке.
        """
        data = {"name": new_name}
        return self.put(f"/folders/{folder_id}", data=data)

    def delete_folder(self, folder_id):
        """
        Удаляет папку по ID.
        :param folder_id: ID папки.
        """
        return self.delete(f"/folders/{folder_id}")
