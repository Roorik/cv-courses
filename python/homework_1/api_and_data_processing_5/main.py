"""Используйте внешний API для получения данных о текущей погоде в заданном городе и сохраните эти данные в файл"""
import json
import logging
import requests

from pathlib import Path

# определяем директорию под чтение и запись файлов, логов
BASE_DIR = Path(__file__).parent
output_dir = BASE_DIR.joinpath('weather.json')
log_dir = BASE_DIR.joinpath('api_log.txt')

# настраиваем логирование
logging.basicConfig(filename=log_dir, level=logging.INFO, filemode='a')
log = logging.getLogger(__name__)

def get_coordinates(city):
    """получаем координаты указанного города"""
    try:
        url = f'https://nominatim.openstreetmap.org/search?q={city}&format=json&limit=1'
        headers = {'User-Agent':'Mozilla/5.0 (compatible; AcmeInc/1.0)'}
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data:
                log.info('Данные от API геокодинга успешно получены')
                return float(data[0]['lat']), float(data[0]['lon'])
    except Exception as e:
        log.error(f'Ошибка на этапе обращения к API геокодинга: {e}')
    return None

def get_weather(city):
    """получаем данные о погоде"""
    try:
        lat, lon = get_coordinates(city)
        if lat and lon:
            url = f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min'
            response = requests.get(url)
            if response.status_code == 200:
                log.info('Данные от API погоды успешно получены')
                return response.json()
        return {}
    except Exception as e:
        log.error(f'Ошибка на этапе обращения к API погоды: {e}')
    return {}


if __name__ == '__main__':
    try:
        city_name = input('Введите название города: ')
        log.info(f'Указано название города: {city_name}')
        weather_data = get_weather(city_name)
        daily = weather_data.get('daily', {}) 
        time = daily.get('time', [])
        temp_min = daily.get('temperature_2m_min', [])
        temp_max = daily.get('temperature_2m_max', [])
        
        data = [
                {
                'city_name': city_name,
                'time': time,
                'temp_min': temp_min,
                'temp_max': temp_max
                }
            ]
        
        with open(output_dir, 'w') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
            log.info(f'Данные получены и записаны в файл {output_dir}')
            log.info(f'Полученные данные: {daily}')
        
    except Exception as e:
        log.error(f'Ошибка на этапе получения данных: {e}')
    
    try:
        ln = min(len(time), len(temp_min), len(temp_max))
        for i in range(ln):
            print(f'Погода {time[i]} ожидается в районе от {temp_min[i]} до {temp_max[i]}')
    except Exception as e:
        log.error(f'Ошибка на этапе перебора списков: {e}')