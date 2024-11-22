'''
Создайте программу, которая вычисляет время восхода и захода солнца для заданной даты и местоположения с использованием модуля PyEphem.
'''
# импортируем нужные либы
import ephem
import logging

from pathlib import Path

# путь для текущей папки
BASE_DIR = Path(__file__).parent
# указываем путь записи логов 
log_dir = BASE_DIR.joinpath('log.txt')

# настраиваем логирование
logging.basicConfig(filename=log_dir, level=logging.INFO, filemode='a')
log = logging.getLogger(__name__)

def main():
    '''
    Мейн функция принимает координаты юзера и выводит время следующего восхода и захода солнца
    
    Return: 
        None
    '''
    # попытка выполнения кода 
    try:
        # запрос ввода широты и долготы у юзера 
        lat = input('Введите широту: ')
        lon = input('Введите долготу: ')
        
        # создаём объект класса observer
        observer = ephem.Observer()
        # передаём атрибуты класса observer: 
        observer.lat = lat # широту
        observer.lon = lon # долготу
        observer.date = ephem.now() # текущую дату
        
        # создание объекта солнца
        sun = ephem.Sun()
        # расчёт времени восхода посредством метода объекта observer
        sunrise = observer.next_rising(sun)
        # расчёт времени захода посредством метода объекта observer
        sunset = observer.next_setting(sun)
        
        # преобразование внутреннего формата времени на локальное юзерское формата питона
        sunrise_time = ephem.localtime(sunrise)
        sunset_time = ephem.localtime(sunset)
        
        # вывод результата
        print(f'Восход солнца: {sunrise_time}')
        print(f'Заход солнца: {sunset_time}')
        
        # запись логов об успешном выполнении программы
        logging.info('Программа успешно отработала')
        logging.info(f'Вычисленное время восхода и захода: {sunrise_time, sunset_time}')
    # если происходит ошибка
    except Exception as e:
        # запись лога ошибки
        logging.error(f'Произошла ошибка: {e}')

if __name__ == '__main__':
    # вызов мейн функции
    main()