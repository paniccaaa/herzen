# Лабораторная работа 3 "Создание своего пакета. Публикация на PyPI"
## Автор: Адаменко Семён Сергеевич, ИВТ 2.1
Итог работы: https://test.pypi.org/project/getweatherdatalr3prog/0.1.1/
токен pypi-AgENdGVzdC5weXBpLm9yZwIkZTNlNGRkM2ItZjVjYi00NDJmLWIwODctODU1ZTBjNDg5MGVhAAIqWzMsImM2ZjdiNDM3LWFlZTEtNGU5Ny1hNWU1LTM2MDdiZTIwMTBmYSJdAAAGIA4Cq59oin1dXxMCPvghrOUT_3-kFGdrcU1qbFQKX9XR
### Описание
Этот проект позволяет получать данные о погоде для заданного города с помощью API OpenWeatherMap. Программа делает HTTP-запросы к API и выводит информацию о погоде в виде JSON-ответа.

### Регистрация
Для использования API OpenWeatherMap необходимо зарегистрироваться на сайте [OpenWeatherMap](https://openweathermap.org/) и получить API-ключ.

Для публикации пакета на Test PyPI:
1. Зарегистрируйтесь на [Test PyPI](https://test.pypi.org/).
2. Получите API-токен для загрузки пакета.

### Ход работы

#### Шаг 1. Установка необходимых инструментов
Для публикации проекта на Test PyPI необходимо установить следующие инструменты:

```bash
pip install setuptools wheel twine
```

#### Шаг 2. Написание [setup.py](setup.py)

#### Шаг 3. Сборка проекта и загрузка на testpypi

```bash
python setup.py sdist bdist_wheel
```

```bash
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```
