from flask import current_app
import requests

def weather_by_city(city_name):
    weather_url = current_app.config['WEATHER_URL']
    params = {
        'city': city_name,
        'country': 'Russia',
        'lang': 'ru',
        'key': current_app.config['WEATHER_API_KEY']
    }
    try:
        result = requests.get(weather_url, params=params)
        result.raise_for_status()
        weather = result.json()
        if 'data' in weather:
            if [0] in weather['data']:
                try:
                    return weather['data'][0]['temp']['app_temp']
                except(IndexError, TypeError):
                    return False
    except(requests.RequestException, ValueError):
        print('Сетевая ошибка')
        return False
    return False

test = weather_by_city('Moscow')
print(test)