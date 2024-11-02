import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr
import os

# Путь к CSV относительно местоположения скрипта
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, 'nyc-rolling-sales.csv')

# Чтение CSV с использованием полного пути
data = pd.read_csv(file_path)
# Очистка данных
data['SALE PRICE'] = pd.to_numeric(data['SALE PRICE'], errors='coerce')
data['GROSS SQUARE FEET'] = pd.to_numeric(data['GROSS SQUARE FEET'], errors='coerce')
data['YEAR BUILT'] = pd.to_numeric(data['YEAR BUILT'], errors='coerce')
data['RESIDENTIAL UNITS'] = pd.to_numeric(data['RESIDENTIAL UNITS'], errors='coerce')

# Очистка данных от строк с NaN значениями
data_clean = data[['GROSS SQUARE FEET', 'YEAR BUILT', 'RESIDENTIAL UNITS', 'SALE PRICE']].dropna()

# Вычисление коэффициентов корреляции
correlation = data_clean.corr()
print("Коэффициенты корреляции:\n", correlation)

# Расчет r для каждой пары переменных
variables = ['GROSS SQUARE FEET', 'YEAR BUILT', 'RESIDENTIAL UNITS']
for var in variables:
    r, _ = pearsonr(data_clean[var], data_clean['SALE PRICE'])
    print(f'Коэффициент корреляции r между {var} и SALE PRICE: {r:.4f}')

# Визуализация: Диаграммы рассеяния
plt.figure(figsize=(15, 5))

# Диаграмма рассеяния: Общая площадь против цены продажи
plt.subplot(1, 3, 1)
sns.scatterplot(data=data_clean, x='GROSS SQUARE FEET', y='SALE PRICE')
plt.title('Общая площадь vs Цена продажи')
plt.xlabel('Общая площадь (кв. футы)')
plt.ylabel('Цена продажи ($)')
plt.xlim(0, data_clean['GROSS SQUARE FEET'].max())
plt.ylim(0, data_clean['SALE PRICE'].max())

# Диаграмма рассеяния: Год постройки против цены продажи
plt.subplot(1, 3, 2)
sns.scatterplot(data=data_clean, x='YEAR BUILT', y='SALE PRICE')
plt.title('Год постройки vs Цена продажи')
plt.xlabel('Год постройки')
plt.ylabel('Цена продажи ($)')
plt.xlim(1900, 2024)  # Установите границы по оси X
plt.ylim(0, data_clean['SALE PRICE'].max())

# Диаграмма рассеяния: Количество жилых единиц против цены продажи
plt.subplot(1, 3, 3)
sns.scatterplot(data=data_clean, x='RESIDENTIAL UNITS', y='SALE PRICE')
plt.title('Количество жилых единиц vs Цена продажи')
plt.xlabel('Количество жилых единиц')
plt.ylabel('Цена продажи ($)')
plt.xlim(0, data_clean['RESIDENTIAL UNITS'].max())
plt.ylim(0, data_clean['SALE PRICE'].max())

# Сохранение всех графиков в один файл
plt.tight_layout()
plt.savefig('scatter_plots.png')  # Сохранение всего рисунка
plt.show()
