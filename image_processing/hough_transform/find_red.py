import cv2
import numpy as np

from skimage import io
from pathlib import Path

BASE_DIR = Path(__file__).parent
res = BASE_DIR.joinpath('result')

def save_image(image, filename):
    """Функция для сохранения изображения."""
    cv2.imwrite(f'{res}_{filename}', image)
    print(f"Изображение сохранено как: {filename}")

def find_color_object(image, lower_bound, upper_bound, output_prefix="result"):
    """
    Функция для поиска объекта по цвету и сохранения изображений.
    
    Параметры:
    - image: входное изображение (в формате BGR)
    - lower_bound: нижний предел цвета в HSV (например, (30, 50, 50))
    - upper_bound: верхний предел цвета в HSV (например, (90, 255, 255))
    - output_prefix: префикс имени выходного файла
    """
    # Переводим изображение из BGR в HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Создаём бинарную маску для заданного диапазона цвета
    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    save_image(mask, f"{output_prefix}_mask.png")
    
    # Морфологическая обработка для удаления шумов
    kernel = np.ones((5, 5), np.uint8)
    mask_cleaned = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    save_image(mask_cleaned, f"{output_prefix}_cleaned_mask.png")
    
    # Поиск контуров
    contours, _ = cv2.findContours(mask_cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Создание изображения с найденными контурами
    result_image = image.copy()
    cv2.drawContours(result_image, contours, -1, (0, 255, 0), 2)
    save_image(result_image, f"{output_prefix}_contours.png")

    print(f"Найдено объектов: {len(contours)}")
    return contours

def main():
    # Загрузка изображения из интернета
    image_url = "https://habrastorage.org/r/w1560/getpro/habr/upload_files/13a/8bb/bb5/13a8bbbb52f60bad2637a2fb6fd3c725.png"
    image = io.imread(image_url)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Определяем границы красного цвета в HSV
    lower_red = (0, 100, 100)  # Нижний порог (оттенок, насыщенность, яркость)
    upper_red = (10, 255, 255)  # Верхний порог

    # Поиск красных объектов и сохранение результатов
    contours = find_color_object(image, lower_red, upper_red, output_prefix="red_object")
    
if __name__ == '__main__':
    main()