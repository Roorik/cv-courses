# Создайте игру, в которой компьютер загадывает число от 1 до 100, а пользователь пытается его угадать.
import random
import logging

from pathlib import Path

# определяем директорию под запись логов
BASE_DIR = Path(__file__).parent
file_dir = BASE_DIR.joinpath('game_log.txt')

# настраиваем логирование
logging.basicConfig(filename=file_dir, level=logging.INFO, filemode='w')

log = logging.getLogger(__name__)

def guess_number(ask_num) -> None:
    flag = True # задаём флаг для окончания цикла
    counter = 0 # задаём счётчик для логирования и финального ответа
    # цикл для перебора ответа юзера
    while flag:
        # получаем ввод от юзера
        try:
            # смотрим больше или меньше
            user_val = int(input('Введите число: '))
            if user_val > ask_num:
                print('Загаданное число меньше')
            elif user_val < ask_num:
                print('Загаданное число больше')
            # если юзер угадал - ставим флаг для завершения цикла
            else:
                flag = False
        # ошибка типа данных
        except ValueError:
            print('Ошибка: неправильный тип данных')
        # счётчик++ и запись лога
        finally:
            counter += 1
            log.info(f'Попытка номер {counter}, введено число {user_val}, правильный ответ - {ask_num}')
    print(f'Победа, количество попыток: {counter}')
    return


if __name__ == '__main__':
    ask_num = random.randint(1, 100)
    guess_number(ask_num)