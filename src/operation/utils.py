import urllib.parse
import requests
from config import WEATHER_API_KEY


class GetWeatherRequest:
    def __init__(self):
        self.session = requests.Session()

    @staticmethod
    def get_weather_url(city):
        base_url = 'https://api.openweathermap.org/data/2.5/weather'
        params = {
            'units': 'metric',
            'q': city,
            'appid': WEATHER_API_KEY
        }
        url = f'{base_url}?{urllib.parse.urlencode(params)}'
        return url

    def send_request(self, url):
        response = self.session.get(url)
        if response.status_code == 200:
            return response
        return None

    @staticmethod
    def get_weather_from_response(response):
        data = response.json()
        return data['main']['temp']

    def get_weather(self, city):
        url = self.get_weather_url(city)
        response = self.send_request(url)
        if response is not None:
            return self.get_weather_from_response(response)
        return None

    def check_existing(self, city):
        url = self.get_weather_url(city)
        response = self.send_request(url)
        return response.status_code == 200
