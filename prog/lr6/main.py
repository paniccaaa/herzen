import io
import requests
import json
import csv
from xml.etree import ElementTree as ET
from abc import ABC, abstractmethod

# Абстрактный интерфейс компонента
class Component(ABC):
    @abstractmethod
    def get_data(self):
        pass

# Базовый компонент - возвращает данные о валютах в формате словаря
class CurrenciesList(Component):
    def get_data(self):
        response = requests.get('http://www.cbr.ru/scripts/XML_daily.asp')
        root = ET.fromstring(response.content)
        currencies = {}
        for valute in root.findall('Valute'):
            charcode = valute.find('CharCode').text
            name = valute.find('Name').text
            value = float(valute.find('Value').text.replace(',', '.'))
            nominal = int(valute.find('Nominal').text)
            currencies[charcode] = {'name': name, 'value': value, 'nominal': nominal}
        return currencies

# Базовый декоратор, который будет изменять компонент
class Decorator(Component): # передаем наш интерфейс с 1 методом
    def __init__(self, component: Component):
        self._component = component

    @abstractmethod
    def get_data(self):
        return self._component.get_data()

# Декоратор для преобразования данных в JSON (расширяем функционал )
class ConcreteDecoratorJSON(Decorator):
    def get_data(self):
        data = self._component.get_data()
        return json.dumps(data, indent=4, ensure_ascii=False)
    
class ConcreteDecoratorCSV(Decorator):
    def get_data(self):
        data = self._component.get_data()

        # Проверка на то, что данные — это словарь
        if isinstance(data, str):
            raise TypeError("cannot apply csv formatting to json string.")
        
        # Используем io.StringIO для записи в строку как в файл
        output = io.StringIO()
        writer = csv.writer(output) # объект для записи данных 

        # Заголовок CSV
        writer.writerow(['CharCode', 'Name', 'Value', 'Nominal'])

        # Данные валют
        for charcode, info in data.items():
            writer.writerow([charcode, info['name'], info['value'], info['nominal']])

        # Получаем строку CSV
        return output.getvalue()


if __name__ == "__main__":
    currencies = CurrenciesList() # является декорируемым

    # Декоратор JSON
    json_decorator = ConcreteDecoratorJSON(currencies) # передаем currencies так как он удовлетворяет интерфейсу Components
    print("JSON format:")
    print(json_decorator.get_data())

    # Декоратор CSV
    csv_decorator = ConcreteDecoratorCSV(currencies) # аналогично 
    print("\nCSV format:")
    print(csv_decorator.get_data())