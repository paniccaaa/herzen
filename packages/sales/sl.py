import os
import pandas as pd
import numpy as np
from scipy.stats import pearsonr

# Определяем путь к CSV относительно местоположения скрипта
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, 'nyc-rolling-sales.csv')

# Загрузка данных из CSV
data = pd.read_csv(file_path)

# Очистка данных: удаляем строки, где 'SALE PRICE' или другие переменные пустые или некорректные
data = data[(data['SALE PRICE'] != ' -  ') & (data['SALE PRICE'].notnull())]
data['SALE PRICE'] = pd.to_numeric(data['SALE PRICE'], errors='coerce')
data['GROSS SQUARE FEET'] = pd.to_numeric(data['GROSS SQUARE FEET'], errors='coerce')
data['YEAR BUILT'] = pd.to_numeric(data['YEAR BUILT'], errors='coerce')
data['RESIDENTIAL UNITS'] = pd.to_numeric(data['RESIDENTIAL UNITS'], errors='coerce')

# Удаление строк с отсутствующими данными в целевых столбцах
data = data.dropna(subset=['SALE PRICE', 'GROSS SQUARE FEET', 'YEAR BUILT', 'RESIDENTIAL UNITS'])

# Функция для расчета коэффициента корреляции Пирсона
def calculate_correlation(data, column1, column2):
    correlation, _ = pearsonr(data[column1], data[column2])
    return correlation

# Расчет коэффициентов корреляции
correlation_gross_sqft = calculate_correlation(data, 'GROSS SQUARE FEET', 'SALE PRICE')
correlation_year_built = calculate_correlation(data, 'YEAR BUILT', 'SALE PRICE')
correlation_residential_units = calculate_correlation(data, 'RESIDENTIAL UNITS', 'SALE PRICE')

# Вывод результатов
print("Коэффициент корреляции между общей площадью и ценой продажи:", correlation_gross_sqft)
print("Коэффициент корреляции между годом постройки и ценой продажи:", correlation_year_built)
print("Коэффициент корреляции между количеством жилых единиц и ценой продажи:", correlation_residential_units)
