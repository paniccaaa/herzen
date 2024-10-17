import io
import requests
import json
import csv
from xml.etree import ElementTree as ET
from abc import ABC, abstractmethod

# Абстрактный интерфейс компонента
class Component(ABC):
    """Абстрактный класс, представляющий интерфейс компонента для получения данных.

    Методы:
        get_data(): Возвращает данные о валютах.
    """
    @abstractmethod
    def get_data(self):
        """Возвращает данные в определённом формате.

        Возвращаемое значение:
            dict: Данные о валютах в формате словаря.
        """
        pass

# Базовый компонент - возвращает данные о валютах в формате словаря
class CurrenciesList(Component):
    """Базовый компонент, возвращающий данные о валютах с сайта ЦБ РФ.

    Методы:
        get_data(): Возвращает данные о валютах в виде словаря с кодом валюты, именем, значением и номиналом.
    """
    def get_data(self):
        """Получает данные о валютах с сайта ЦБ РФ.

        Возвращаемое значение:
            dict: Словарь с данными о валютах, где ключ — это код валюты, а значение — информация о валюте (имя, значение, номинал).
        """
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
class Decorator(Component):
    """Абстрактный декоратор для компонентов.

    Атрибуты:
        _component (Component): Компонент, который будет декорирован.

    Методы:
        get_data(): Получает данные компонента.
    """
    def __init__(self, component: Component):
        """Инициализирует декоратор с компонентом.

        Args:
            component (Component): Компонент для декорирования.
        """
        self._component = component

    @abstractmethod
    def get_data(self):
        """Вызывает метод get_data декорируемого компонента.

        Возвращаемое значение:
            dict: Данные, возвращаемые декорируемым компонентом.
        """
        return self._component.get_data()

# Декоратор для преобразования данных в JSON (расширяем функционал )
class ConcreteDecoratorJSON(Decorator):
    """Декоратор, который преобразует данные компонента в JSON-формат.

    Методы:
        get_data(): Возвращает данные в формате JSON.
    """
    def get_data(self):
        """Преобразует данные компонента в JSON-формат.

        Возвращаемое значение:
            str: Данные в формате JSON.
        """
        data = self._component.get_data()
        return json.dumps(data, indent=4, ensure_ascii=False)
    
class ConcreteDecoratorCSV(Decorator):
    """Декоратор, который преобразует данные компонента в CSV-формат.

    Методы:
        get_data(): Возвращает данные в формате CSV.
    """
    def get_data(self):
        """Преобразует данные компонента в CSV-формат.

        Возвращаемое значение:
            str: Данные в формате CSV.

        Исключения:
            TypeError: Выбрасывается, если данные переданы в виде строки (JSON).
        """
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
    currencies = CurrenciesList()  # является декорируемым

    # Декоратор JSON
    json_decorator = ConcreteDecoratorJSON(currencies)  # передаем currencies, так как он удовлетворяет интерфейсу Component
    print("JSON format:")
    print(json_decorator.get_data())

    # Декоратор CSV
    csv_decorator = ConcreteDecoratorCSV(currencies)  # аналогично
    print("\nCSV format:")
    print(csv_decorator.get_data())
