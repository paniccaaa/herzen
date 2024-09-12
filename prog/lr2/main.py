from getweatherdata import get_weather_data

owm_api_key = '913df8b0a3e193154f2ea113ceb61e61'

if __name__ == '__main__':
    city = 'Moscow'
    data = get_weather_data(city, api_key=owm_api_key)
    if data:
        print(data)
    else:
        print("Не удалось получить данные о погоде.")
