import requests
import json

def get_weather_data(place, api_key=None):
    if not api_key:
        print("API ключ не задан.")
        return None

    try:
        response = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather',
            params={'q': place, 'appid': api_key, 'units': 'metric'}
        )
        response.raise_for_status() 
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе данных: {e}")
        return None
