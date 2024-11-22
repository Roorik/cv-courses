'''
Создайте программу, которая открывает окно и отображает движущийся круг с использованием модуля pygame.
'''
# импортируем нужные либы
import sys
import pygame
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
    Мейн функция инициализирует и запускает окно приложения с движущимся мячом 
    
    Return: 
        None
    '''
    try:
        # запуск модуля pygame
        pygame.init()
        
        size = width, height = 800, 600 # устанавливаем размер окна приложения
        speed = [1, 1] # устанавливаем скорость мяча по двум координатам
        black = 0, 0, 0 # устанавливаем значения ргб для чёрного цвета
        
        # создаём экран и задаём ему размер 
        screen = pygame.display.set_mode(size)
        # создаём мяч размером 50х50 и добавляем альфа-канал
        ball = pygame.Surface((50, 50), pygame.SRCALPHA)
        # отрисовываем мяч в виде круга 
        pygame.draw.circle(ball, (255, 0, 0), (15, 15), 25) #(спрайт мяча, цвет, центр спрайта в координатах, скругление)
        # задаём мячу поведение
        ballrect = ball.get_rect()
        # бесконечный цикл
        while True:
            # сверяемся с происходящим в приложении событием
            for event in pygame.event.get():
                # если событие выход
                if event.type == pygame.QUIT:
                    # завершаем программу и даём системе знать об этом
                    pygame.quit() 
                    sys.exit()
            # заставляем мяч двигаться с заданной скоростью
            ballrect = ballrect.move(speed)
            # если координата меньше нуля слева или больше ширины окна справа
            if ballrect.left < 0 or ballrect.right > width: 
                speed[0] = -speed[0] # меняем вектор по оси X на противоположный
            # если координата меньше нуля сверху или больше высоты окна снизу
            if ballrect.top < 0 or ballrect.bottom > height: 
                speed[1] = -speed[1] # меняем вектор по оси Y на противоположный
            # очищаем экран
            screen.fill(black)
            # отрисовываем мяч в новом положении
            screen.blit(ball, ballrect)
            # обновляем дисплей
            pygame.display.flip()

    # если происходит ошибка
    except Exception as e:
        # запись лога ошибки
        log.error(f'Произошла ошибка: {e}')

if __name__ == '__main__':
    # вызов мейн функции
    main()