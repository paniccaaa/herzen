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

# Абстрактный интерфейс для Наблюдателей
class Observer(ABC):
    @abstractmethod
    async def update(self, message: str):
        """Метод для обновления данных у наблюдателя."""
        pass

# Абстрактный интерфейс для Субъектов
class Subject(ABC):
    @abstractmethod
    def subscribe(self, observer: Observer):
        """Добавляет наблюдателя в список подписчиков."""
        pass

    @abstractmethod
    def unsubscribe(self, observer: Observer):
        """Удаляет наблюдателя из списка подписчиков."""
        pass

    @abstractmethod
    def notify(self, message: str):
        """Уведомляет всех наблюдателей о событии."""
        pass

# Класс для получения данных о курсах валют
class CurrenciesList(Subject):
    def __init__(self):
        self._observers = []  # Список наблюдателей (клиентов)
    
    def subscribe(self, observer: Observer):
        """Подписка на обновления."""
        self._observers.append(observer)

    def unsubscribe(self, observer: Observer):
        """Отписка от обновлений."""
        self._observers.remove(observer)

    async def notify(self, message: str):
        """Оповещение всех наблюдателей."""
        for observer in self._observers:
            await observer.update(message)  

    def get_data(self):
        """Запрашивает данные о курсах валют с API Центробанка России."""
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

    async def update_data(self):
        """Периодическое обновление данных и уведомление подписчиков."""
        currencies = self.get_data()
        if currencies:
            json_data = json.dumps(currencies)
            await self.notify(json_data)  # Уведомляем всех подписчиков о новых данных

# (Наблюдатели)
class WebSocketClient(Observer):
    def __init__(self, websocket: WebSocket):
        self.websocket = websocket
    
    async def update(self, message: str):
        """Метод обновления данных для WebSocket-клиента."""
        await self.websocket.send_text(message)

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
    """Обрабатывает WebSocket-соединения от клиентов."""
    await websocket.accept()  # Принять WebSocket-соединение
    client = WebSocketClient(websocket)  # Создаем клиента-обсервер
    clients.append(client)  # Подписываем клиента на обновления

    # Подписываем клиента на обновления данных
    currency_data.subscribe(client)

    try:
        while True:
            await websocket.receive_text()  # Ожидание сообщений от клиента
    except Exception:
        clients.remove(client)  # Удаление клиента в случае ошибки
        currency_data.unsubscribe(client)  # Отписка от обновлений

async def currency_updater():
    """Периодически обновляет курсы валют и уведомляет клиентов."""
    while True:
        await currency_data.update_data()  # Обновляем курсы валют и уведомляем подписчиков
        await asyncio.sleep(20)  # Запрос каждые 20 секунд

@app.on_event("startup")
async def startup_event():
    """Запускаем задачу обновления курсов валют при старте приложения."""
    global currency_data
    currency_data = CurrenciesList()  # Создаем объект для получения курсов валют
    task = asyncio.create_task(currency_updater())  # Запускаем задачу обновления данных

@app.on_event("shutdown")
async def shutdown_event():
    """Закрываем все WebSocket-соединения при остановке приложения."""
    for client in clients:
        await client.websocket.close()  # Закрытие WebSocket-соединений

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)  # Запуск приложения
