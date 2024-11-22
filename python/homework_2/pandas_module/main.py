'''
Создайте программу, которая считывает данные из CSV-файла data.csv, выполняет простую обработку данных и выводит результат. 
Используйте модуль pandas для работы с данными.
'''
# импортируем нужные либы
import pandas as pd
import logging

from pathlib import Path

# путь для текущей папки
BASE_DIR = Path(__file__).parent
# указываем путь чтения документа
input_dir = BASE_DIR.joinpath('data.csv')
# указываем путь записи логов 
log_dir = BASE_DIR.joinpath('log.txt')

# настраиваем логирование
logging.basicConfig(filename=log_dir, level=logging.INFO, filemode='a')
log = logging.getLogger(__name__)

def main():
    '''
    Мейн функция считывает данные CSV файла, подсчитывает общую выручку в нём и выводит в консоль
    
    Return: 
        None
    '''
    # попытка выполнения кода 
    try:
        # читаем csv файл и записываем в переменную датафрейма 
        df = pd.read_csv(input_dir)
        # запись в новый столбец произведения проданных товаров и их прайса в соответствующей строке
        df['Revenue'] = df['Units Sold'] * df['Unit Price']
        # запись в отдельную переменную общей выручки
        total_revenue = df['Revenue'].sum()
    
        print(df) # вывод переменной датафрейма
        print(f'\nОбщая выручка: {total_revenue}') # вывод общей выручки
        
        # запись логов об успешном выполнении программы
        log.info('Данные успешно обработаны')
        log.info(f'Общая выручка: {total_revenue}')
    # если читаемый файл не найден
    except FileNotFoundError:
        log.error('Файл data.csv не найден') # запись лога ошибки
    # если какая-л другая ошибка
    except Exception as e:
        log.error(f'Произошла ошибка: {e}') # запись лога ошибки

if __name__ == '__main__':
    # вызов мейн функции
    main()