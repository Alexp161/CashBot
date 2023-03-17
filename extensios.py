import requests
import json
from config import names  # импортируем словарь валют из файла config.py

# Определяем собственное исключение для обработки ошибок
class APIException(Exception):
    pass

# Класс Converter для работы с API конвертера валют
class Converter():
    # Базовый URL для запросов API
    BASE_URL = "https://v6.exchangerate-api.com/v6/de786207f7a1793a9b08c2c4/latest/{base}"

    # Метод для проверки корректности входных данных
    @staticmethod
    def validate_input(base, quote, amount):
        if base == quote:
            # Валюты должны отличаться друг от друга
            raise APIException(f"Невозможно конвертировать {base} одинаковые валюты ")

        if base not in names:
            # Проверяем, что введенная валюта поддерживается API
            raise APIException(f"{base} Не удалось обработать валюту. Поддерживаемые валюты: {', '.join(names)}")

        if quote not in names:
            # Проверяем, что введенная валюта поддерживается API
            raise APIException(f"{quote} Не удалось обработать валюту. Поддерживаемые валюты: {', '.join(names)}")

        try:
            # Проверяем, что количество является числом
            float(amount)
        except ValueError:
            raise APIException(f"{amount} Не удалось обработать количество")

    # Метод для получения курса валют и конвертации введенной суммы
    @staticmethod
    def get_price(base, quote, amount):
        # Проверяем корректность входных данных
        Converter.validate_input(base, quote, amount)

        url = Converter.BASE_URL.format(base=names[base])
        # Параметры запроса API
        params = {
            "access_key": "de786207f7a1793a9b08c2c4",
            "currencies": names[quote],
            "source": names[base],
            "format": 1
        }

        try:
            # Отправляем запрос API
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            # Обрабатываем ошибки сети (например, отсутствие интернет-соединения)
            raise APIException(f"Ошибка сети: {str(e)}")
        except json.JSONDecodeError as e:
            # Обрабатываем ошибки декодирования JSON
            raise APIException(f"Ошибка декодирования JSON: {str(e)}")

        if "error" in data:
            raise APIException(data["error"]["info"])

        rate = data["conversion_rates"][names[quote]]
        converted_amount = float(amount) * rate

        return converted_amount
