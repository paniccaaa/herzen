# Лабораторная работа 2 "Использование API openweathermap.org"
## Работу выполнил: Адаменко Семён Сергеевич, ИВТ 2.1

### Регистрация 
Для начала необходимо зарегистрироваться в https://home.openweathermap.org/ и получить API key

### Напишем функцию для получения погоды и обработаем ошибки:
```python
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
        response.raise_for_status()  # Проверка на HTTP ошибки
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе данных: {e}")
        return None

```

### Тесты
```python
# test_getweatherdata.py
import pytest
import json
from getweatherdata import get_weather_data

key = '913df8b0a3e193154f2ea113ceb61e61'

def test_without_key():
    assert get_weather_data("Moscow") is None, \
        "Для получения данных необходимо задать значение для api_key"

def test_in_riga():
    assert get_weather_data("Riga", api_key=key) is not None, \
        "Response is None while using the key"

def test_type_of_res():
    assert isinstance(get_weather_data("Riga", api_key=key), str), \
        "Response is not of type string while using the key"

def test_args_error():
    assert get_weather_data('') is None, \
        "There should be one positional argument: 'city' and one keyword argument 'api_key'"

def test_coords_dim():
    data = json.loads(get_weather_data('Riga', api_key=key))
    assert len(data.get('coord', {})) == 2, "Dimension is 2: lon and lat"

def test_temp_type():
    data = json.loads(get_weather_data('Riga', api_key=key))
    assert isinstance(data.get('main', {}).get('feels_like'), float), \
        "Error with type of feels_like attribute"

inp_params_1 = "city, api_key, expected_country"
exp_params_countries = [
    ("Chicago", key, 'US'),
    ("Saint Petersburg", key, 'RU'),
    ("Dhaka", key, 'BD'),
    ("Minsk", key, 'BY'),
    ("Kyoto", key, 'JP'),
    ("Anchorage", key, 'US'),
    ("Havana", key, 'CU')
]

@pytest.mark.parametrize(inp_params_1, exp_params_countries)
def test_countries(city, api_key, expected_country):
    data = json.loads(get_weather_data(city, api_key=key))
    assert data.get('sys', {}).get('country', 'NoValue') == expected_country, \
        "Error with country code"

```

### И главный main.py
```python
from getweatherdata import get_weather_data

# Замените на ваш реальный ключ API
owm_api_key = ''

if __name__ == '__main__':
    city = 'Moscow'
    data = get_weather_data(city, api_key=owm_api_key)
    if data:
        print(data)
    else:
        print("Не удалось получить данные о погоде.")
```


### Пример запроса
```sh
❯ python prog/lr2/main.py
{"coord":{"lon":37.6156,"lat":55.7522},"weather":[{"id":804,"main":"Clouds","description":"overcast clouds","icon":"04d"}],"base":"stations","main":{"temp":20.8,"feels_like":19.69,"temp_min":20.1,"temp_max":21.24,"pressure":1018,"humidity":29,"sea_level":1018,"grnd_level":999},"visibility":10000,"wind":{"speed":6.39,"deg":145,"gust":9.42},"clouds":{"all":97},"dt":1726132336,"sys":{"type":1,"id":9027,"country":"RU","sunrise":1726109763,"sunset":1726156545},"timezone":10800,"id":524901,"name":"Moscow","cod":200}
```