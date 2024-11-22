'''
Создайте программу, которая выводит сообщение пользователя с использованием ASCIIарта из модуля cowsay. 
Пользователь вводит сообщение, и программа отображает корову, "произносящую" это сообщение.
'''
# импортируем нужные либы
import cowsay
import logging

from pathlib import Path

# путь для текущей папки
BASE_DIR = Path(__file__).parent
# указываем путь записи логов 
log_dir = BASE_DIR.joinpath('log.txt')

# настраиваем логирование
logging.basicConfig(filename=log_dir, level=logging.INFO, filemode='a')
log = logging.getLogger(__name__)

def main() -> None:
    '''
    Мейн функция принимает сообщение юзера и выводит в формате ascii арта
    
    Return: 
        None
    '''
    # попытка выполнения кода
    try:
        # ввод сообщения юзера
        message: str = input('Введите ваше сообщение: ')
        # вызываем функцию miki модуля cowsay, передаём в параметры сообщение юзера
        cowsay.miki(message)
        # запись логов об успешном выполнении программы
        log.info('Программа успешно выполнена')
        log.info(f'Введена фраза: {message}')
    # если происходит ошибка
    except Exception as e:
        # запись лога ошибки
        log.error(f'Произошла ошибка: {e}')


if __name__ == '__main__':
    # вызов мейн функции
    main()