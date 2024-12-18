'''
Создайте программу, которая генерирует массив случайных чисел, вычисляет их среднее
значение и стандартное отклонение. Используйте модуль numpy.
'''
# импортируем нужные либы
import logging
import numpy as np

from pathlib import Path

# путь для текущей папки
BASE_DIR = Path(__file__).parent
# указываем путь записи логов 
log_dir = BASE_DIR.joinpath('log.txt')

# настраиваем логирование
logging.basicConfig(filename=log_dir, level=logging.INFO, filemode='w')
log = logging.getLogger(__name__)

def main() -> None:
    """
    Мейн функция генерирует 100 рандомных значений и вычисляет среднее и стандартное отклонение
    """
    # попытка выполнения кода
    try:
        # объявляем переменную с типом массива np и задаём ей массив из 100 рандомных знаечний
        data: np.ndarray = np.random.rand(100)  
        # вычисляем среднее знчение с типом с плавающей точкой
        mean: float = np.mean(data)
        # вычисляем стандартное отклонение с типом с плавающей точкой
        std_dev: float = np.std(data)
        
        # выводим результат в консоль
        print(f'Среднее значение: {mean}')
        print(f'Стандартное отклонение: {std_dev}')
        # запись логов с массивом, результатами и об успешном выполнении программы
        log.info(f'Массив: {data}')
        log.info(f'Результаты: {mean}, {std_dev}')
        log.info('Вычисления успешно выполнены')
    # если происходит ошибка
    except Exception as e:
        # запись лога ошибки
        log.error(f'Произошла ошибка: {e}')


if __name__ == '__main__':
    # вызов мейн функции
    main()