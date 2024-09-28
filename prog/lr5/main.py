import requests
from xml.etree import ElementTree as ET
import time
import matplotlib.pyplot as plt
from datetime import datetime


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class CurrencyManager(metaclass=SingletonMeta):
    def __init__(self):
        self._currencies = {}
        self._last_request_time = 0
        self._request_interval = 1  # время в секундах между запросами

    def get_currencies(self, currencies_ids_lst: list) -> list:
        """Получение курсов валют с сайта ЦБ"""
        # Реализация 5 пункта (контроль запросов)
        current_time = time.time()
        if current_time - self._last_request_time < self._request_interval:
            raise Exception("Запрос слишком частый, подождите")

        self._last_request_time = current_time
        cur_res_str = requests.get('http://www.cbr.ru/scripts/XML_daily.asp')
        result = []

        root = ET.fromstring(cur_res_str.content)
        valutes = root.findall("Valute")

        for _v in valutes:
            valute_id = _v.get('ID')
            if valute_id in currencies_ids_lst:
                name = _v.find('Name').text
                value = _v.find('Value').text.replace(',', '.')
                nominal = int(_v.find('Nominal').text)
                charcode = _v.find('CharCode').text

                # Разделяем целую и дробную часть
                value_float = float(value)
                whole, fraction = divmod(value_float * nominal, 1)

                self._currencies[charcode] = {
                    'name': name,
                    'value': (int(whole), int(fraction * 10000)),  # сохраняем значение в виде (целая, дробная)
                    'nominal': nominal
                }

                result.append({charcode: (name, f'{int(whole)},{int(fraction * 10000)}')})

        if not result:
            return {'R9999': None}
        return result

    def visualize_currencies(self):
        """Визуализация курсов валют"""
        if not self._currencies:
            raise Exception("Нет данных для визуализации")

        currencies_names = []
        currencies_values = []

        for charcode, data in self._currencies.items():
            currencies_names.append(charcode)
            value = data['value']
            currencies_values.append(float(f'{value[0]}.{value[1]}'))

        fig, ax = plt.subplots()
        ax.bar(currencies_names, currencies_values, color='tab:blue')

        ax.set_ylabel('Курс валюты')
        ax.set_title(f'Курсы валют на {datetime.now().strftime("%d-%m-%Y")}')
        plt.savefig('prog/lr5/currencies.jpg')
        plt.show()

def test_invalid_currency():
    manager = CurrencyManager()
    result = manager.get_currencies(['R9999'])
    time.sleep(1)
    assert result == {'R9999': None}

def test_valid_currency():
    manager = CurrencyManager()
    result = manager.get_currencies(['R01035'])
    assert 'GBP' in result[0]

if __name__ == '__main__':
    manager = CurrencyManager()

    try:
        # Получаем список валют по ID
        currencies = manager.get_currencies(['R01035', 'R01335', 'R01700J'])
        print(currencies)

        # Визуализируем данные
        manager.visualize_currencies()
    except Exception as e:
        print(e)
