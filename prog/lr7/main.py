import io
import requests
import json
import csv
from xml.etree import ElementTree as ET
from abc import ABC, abstractmethod
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import random

# Абстрактный интерфейс компонента
class Component(ABC):
    @abstractmethod
    def get_data(self):
        """Абстрактный метод для получения данных о курсах валют."""
        pass

class CurrenciesList(Component):
    def get_data(self):
        """Запрашивает данные о курсах валют с API Центробанка России.
        
        Возвращает словарь с курсами валют или пустой словарь в случае ошибки.
        """
        try:
            response = requests.get('http://www.cbr.ru/scripts/XML_daily.asp')
            response.raise_for_status()  # Проверка на ошибки в HTTP-запросе
            root = ET.fromstring(response.content)
            currencies = {}
            for valute in root.findall('Valute'):
                charcode = valute.find('CharCode').text  # Получение кода валюты
                name = valute.find('Name').text  # Получение названия валюты
                value = float(valute.find('Value').text.replace(',', '.'))  # Получение значения валюты
                nominal = int(valute.find('Nominal').text)  # Получение номинала валюты
                currencies[charcode] = {'name': name, 'value': value, 'nominal': nominal}
            return currencies
        except requests.RequestException as e:
            print(f"Ошибка при запросе курсов валют: {e}")
            return {}  # Возврат пустого словаря в случае ошибки

class Decorator(Component):
    def __init__(self, component: Component):
        """Инициализирует декоратор с компонентом."""
        self._component = component

class ConcreteDecoratorJSON(Decorator):
    def get_data(self):
        """Возвращает данные о курсах валют в формате JSON."""
        data = self._component.get_data() 
        return json.dumps(data, indent=4, ensure_ascii=False)  

class ConcreteDecoratorCSV(Decorator):
    def get_data(self):
        """Возвращает данные о курсах валют в формате CSV."""
        data = self._component.get_data() 
        if isinstance(data, str):
            raise TypeError("Cannot apply CSV formatting to JSON string.")
        
        output = io.StringIO() 
        writer = csv.writer(output)
        writer.writerow(['CharCode', 'Name', 'Value', 'Nominal'])  
        for charcode, info in data.items():
            writer.writerow([charcode, info['name'], info['value'], info['nominal']])
        return output.getvalue()  # Возврат CSV-строки

# Настройка FastAPI приложения
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

clients = []

# HTML-контент для клиентского интерфейса
html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Currency Observer</title>
    <script>
        var ws = new WebSocket("ws://localhost:8000/ws");  // Установление WebSocket-соединения
        ws.onmessage = function(event) {
            var message = JSON.parse(event.data);  // Парсинг полученного сообщения
            var output = document.getElementById("output");
            output.innerHTML = JSON.stringify(message, null, 4);  // Отображение данных на странице
        };
    </script>
</head>
<body>
    <h1>Currency Observer</h1>
    <h2>Client ID: <span id="client-id"></span></h2>
    <pre id="output"></pre>
    <script>
        // Генерация уникального идентификатора клиента
        document.getElementById("client-id").innerText = Math.random().toString(36).substr(2, 9);
    </script>
</body>
</html>
"""

@app.get("/")
async def root():
    """Возвращает HTML-контент для клиентского интерфейса."""
    return HTMLResponse(html_content)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Обрабатывает WebSocket-соединения от клиентов.
    
    Принимает клиента и добавляет его в список подключённых клиентов.
    """
    await websocket.accept()  # Принять WebSocket-соединение
    clients.append(websocket)  # Добавить клиента в список
    try:
        while True:
            await websocket.receive_text()  # Ожидание сообщений от клиента
    except Exception:
        clients.remove(websocket)  # Удаление клиента в случае ошибки

async def notify_clients(message):
    """Уведомляет всех подключённых клиентов о новых данных."""
    for client in clients:
        await client.send_text(message)  # Отправка сообщения каждому клиенту

async def currency_updater():
    """Периодически обновляет курсы валют и уведомляет клиентов."""
    currencies = CurrenciesList()  # Создание объекта для получения курсов валют
    while True:
        data = currencies.get_data()  # Запрос курсов валют
        if data:  # Проверка на наличие данных
            json_data = json.dumps(data) 
            await notify_clients(json_data)  # Уведомление клиентов
        await asyncio.sleep(20)  # Запрос каждые 20 секунд

@app.on_event("startup")
async def startup_event():
    """Событие, запускаемое при старте приложения.
    
    Запускает задачу обновления курсов валют.
    """
    task = asyncio.create_task(currency_updater())

@app.on_event("shutdown")
async def shutdown_event():
    """Событие, запускаемое при остановке приложения.
    
    Закрывает все WebSocket-соединения.
    """
    for client in clients:
        await client.close()  # Закрытие WebSocket-соединений

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)  # Запуск приложения на указанном хосте и порту
