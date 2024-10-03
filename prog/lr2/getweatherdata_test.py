# test_getweatherdata.py
import pytest
import json
from getweatherdata import get_weather_data

# your api key here
key = ''

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

@pytest.mark.parametrize(inp_params_1, exp_params_countries) # декоратор для параметризации тестов
def test_countries(city, api_key, expected_country):
    data = json.loads(get_weather_data(city, api_key=key)) # json str -> python dict
    # ожидается что значение country должно совпадать с expected_country
    assert data.get('sys', {}).get('country', 'NoValue') == expected_country, \
        "Error with country code"
