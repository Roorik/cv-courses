# У вас есть файл `employees.json`, содержащий информацию о сотрудниках: имя, возраст, должность и зарплата. 
# Необходимо обработать эти данные и вывести список сотрудников, чья зарплата выше среднего.

import json
import logging

from pathlib import Path

# определяем директорию под чтение и запись файлов, логов
BASE_DIR = Path(__file__).parent
employees_dir = BASE_DIR.joinpath('employees.json')
earners_dir = BASE_DIR.joinpath('high_earners.json')
log_dir = BASE_DIR.joinpath('processing_log.txt')

# настраиваем логирование
logging.basicConfig(filename=log_dir, level=logging.INFO, filemode='w')
log = logging.getLogger(__name__)

# здесь будет фильтроваться лист работников
def filter_employees(data) -> list:
    # вычисляем среднюю зп
    avarage_salary = sum(employee['salary'] for employee in data) / len(data)
    # фильтруем работников с зп выше средней
    res = [employee for employee in data if employee['salary'] > avarage_salary]
    
    return res

if __name__ == '__main__':
    # выполняем программу
    try:
        # пытаемся открыть файл по заданной директории с входными данными
        try:
            with open(employees_dir, 'r') as input_file:
                # выгружаем данные в переменную 
                data = json.load(input_file)
        except:
            log.error(f'Файл {employees_dir} не найден')

        # достаём из полученных данных лист работников, при отсутствии такого списка отдаём пустой лист
        list_employees = data.get('employees', [])
        # вызываем функцию фильтрации и передаём полученные данные
        high_earners = filter_employees(list_employees) if list_employees != [] else log.error(f'Данные в файле {employees_dir} отсутствуют')

        # открываем файл для записи результата
        with open(earners_dir, 'w', encoding='utf-8') as output_file:
            json.dump(high_earners, output_file, ensure_ascii=False, indent=4)
        
        log.info(f'Количество сотрудников - {len(high_earners)}')    
        # перебираем лист результата для вывода и записи каждого отдельного работника
        for employee in high_earners:
            name = employee['name']
            position = employee['position']
            salary = employee['salary']
            
            print(f'{name} - {position} - {salary}p.')
            log.info(f'{name} - {position} - {salary}p.')
            
    # если в программе что-то пойдёт не так
    except Exception as e:
        log.error(f'Произошла ошибка: {e}')
    