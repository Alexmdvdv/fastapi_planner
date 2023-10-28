import urllib.parse

import requests

WEATHER_API_KEY = '99ba78ee79a2a24bc507362c5288a81b'


class GetWeatherRequest:
    """
    Выполняет запрос на получение текущей погоды для города
    """

    def __init__(self):
        """
        Инициализирует класс
        """
        self.session = requests.Session()

    @staticmethod
    def get_weather_url(city):
        """
        Генерирует url включая в него необходимые параметры
        Args:
            city: Город
        Returns:
            url: Сформированный URL для запроса
        """
        base_url = 'https://api.openweathermap.org/data/2.5/weather'
        params = {
            'units': 'metric',
            'q': city,
            'appid': WEATHER_API_KEY
        }
        url = f'{base_url}?{urllib.parse.urlencode(params)}'
        return url

    def send_request(self, url):
        """
        Отправляет запрос на сервер
        Args:
            url: Адрес запроса
        Returns:
             response: Ответ от сервера
        """
        response = self.session.get(url)
        if response.status_code == 200:
            return response
        return None

    @staticmethod
    def get_weather_from_response(response):
        """
        Достает погоду из ответа
        Args:
            response: Ответ, пришедший с сервера
        Returns:
            Текущая температура
        """
        data = response.json()
        print(data)
        return data['main']['temp']

    def get_weather(self, city):
        """
        Делает запрос на получение погоды
        Args:
            city: Город
        Returns:
            Текущая температура
        """
        url = self.get_weather_url(city)
        response = self.send_request(url)
        if response is not None:
            return self.get_weather_from_response(response)
        return None

    def check_existing(self, city):
        """
        Проверяет наличие города
        Args:
            city: Название города
        Returns:
            True, если город существует, иначе None
        """
        url = self.get_weather_url(city)
        response = self.send_request(url)
        return response.status_code == 200
