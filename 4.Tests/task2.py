import requests
import pytest
import os
from dotenv import load_dotenv

load_dotenv()


class TestYandexDiskAPI:
    """Тесты для Яндекс.Диск REST API"""

    # Получите токен из переменной окружения или замените на свой
    BASE_URL = "https://cloud-api.yandex.net/v1/disk/resources"
    TOKEN = os.getenv("YANDEX_TOKEN")

    # Папка для тестирования
    TEST_FOLDER = "test_folder_api"

    def setup_method(self):
        """Настройка перед каждым тестом"""
        if not self.TOKEN:
            pytest.skip(
                "Токен Яндекс.Диск не установлен. "
                "Установите переменную окружения YANDEX_TOKEN"
            )

        self.headers = {"Authorization": f"OAuth {self.TOKEN}"}

    def teardown_method(self):
        """Очистка после каждого теста - удаляем тестовую папку"""
        try:
            requests.delete(
                f"{self.BASE_URL}?path={self.TEST_FOLDER}", headers=self.headers
            )
        except:
            pass

    def test_create_folder_success(self):
        """Позитивный тест: успешное создание папки"""
        response = requests.put(
            f"{self.BASE_URL}?path={self.TEST_FOLDER}", headers=self.headers
        )

        assert response.status_code == 201, (
            f"Ожидался код 201, получен {response.status_code}. "
            f"Ответ: {response.text}"
        )

        response = requests.get(
            f"{self.BASE_URL}?path={self.TEST_FOLDER}", headers=self.headers
        )

        assert response.status_code == 200, (
            f"Не удалось получить информацию о созданной папке. "
            f"Код: {response.status_code}"
        )

        data = response.json()
        assert data["type"] == "dir", "Созданный ресурс не является папкой"
        assert data["name"] == self.TEST_FOLDER, "Имя папки не совпадает"

    def test_create_folder_already_exists(self):
        """Негативный тест: попытка создать папку, которая уже существует"""
        # Сначала создаем папку
        requests.put(f"{self.BASE_URL}?path={self.TEST_FOLDER}", headers=self.headers)

        response = requests.put(
            f"{self.BASE_URL}?path={self.TEST_FOLDER}", headers=self.headers
        )

        assert response.status_code == 409, (
            f"Ожидалась ошибка 409 при создании существующей папки, "
            f"получен {response.status_code}"
        )

    def test_create_folder_without_auth(self):
        """Негативный тест: создание папки без авторизации"""
        response = requests.put(
            f"{self.BASE_URL}?path={self.TEST_FOLDER}",
            headers={"Authorization": "OAuth invalid_token"},
        )

        assert response.status_code == 401, (
            f"Ожидалась ошибка 401 без авторизации, " f"получен {response.status_code}"
        )

    def test_create_folder_empty_name(self):
        """Негативный тест: создание папки с пустым именем"""
        response = requests.put(f"{self.BASE_URL}?path=", headers=self.headers)

        assert response.status_code >= 400, (
            f"Ожидалась ошибка для пустого имени, " f"получен {response.status_code}"
        )


if __name__ == "__main__":
    print("Запуск тестов Яндекс.Диск API...")
