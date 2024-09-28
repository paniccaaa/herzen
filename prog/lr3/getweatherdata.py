import requests

def get_weather_data(place, api_key=None):
    if not api_key:
        print("API ключ не задан.")
        return None

    try:
        response = requests.get(
            'https://api.openweathermap.org/data/2.5/weather',
            params={'q': place, 'appid': api_key, 'units': 'metric'}
        )
        response.raise_for_status()  # Проброс ошибки HTTP
        print(f"HTTP статус: {response.status_code}")
        return response.text
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP ошибка: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Ошибка при запросе: {req_err}")
    return None
