from api_client import ApiClient
from api_user import UserApi

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

    def rename_folder(self, folder_id, new_name):
        """
        Переименовывает папку.
        :param folder_id: ID папки.
        :param new_name: Новое название папки.
        :return: True, если переименование успешно, False в противном случае.
        """
        data = {"name": new_name}
        response = self.put(f"/folders/{folder_id}", data=data)
        return response["success"]

    def delete_folder(self, folder_id):
        """
        Удаляет папку.
        :param folder_id: ID папки.
        :return: True, если удаление успешно, False в противном случае.
        """
        response = self.delete(f"/folders/{folder_id}")
        return response["success"]

    def get_folder_info(self, folder_id):
        """
        Получает информацию о папке.
        :param folder_id: ID папки.
        :return: Информация о папке в виде словаря.
        """
        response = self.get(f"/folders/{folder_id}")
        return response
