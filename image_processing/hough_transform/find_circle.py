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

def detect_circles(image, dp=1.2, min_dist=100, param1=50, param2=50, min_radius=30, max_radius=70, output_prefix="circles"):
    """
    Функция для обнаружения кругов на изображении с использованием преобразования Хафа.
    
    Параметры:
    - image: входное изображение (в формате BGR)
    - dp: разрешение обнаружения (чем больше, тем меньше разрешение)
    - min_dist: минимальное расстояние между кругами
    - param1: порог для градиента Кэнни
    - param2: порог для метода Хафа
    - min_radius: минимальный радиус круга
    - max_radius: максимальный радиус круга
    - output_prefix: префикс имени выходного файла
    """

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    
    circles = cv2.HoughCircles(
        gray,
        cv2.HOUGH_GRADIENT,
        dp,
        min_dist,
        param1=param1,
        param2=param2,
        minRadius=min_radius,
        maxRadius=max_radius
    )

    result_image = image.copy()

    # Если круги найдены, рисуем их
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for (x, y, r) in circles[0, :]:
            cv2.circle(result_image, (x, y), r, (0, 255, 0), 2)
            cv2.circle(result_image, (x, y), 2, (0, 0, 255), 3)

        save_image(result_image, f"{output_prefix}_detected_circles.png")
        print(f"Найдено кругов: {len(circles[0])}")
    else:
        print("Круги не найдены.")
        save_image(result_image, f"{output_prefix}_no_circles.png")

    return circles

def main():

    # Загрузка изображения из интернета
    image_url = "https://thumbs.dreamstime.com/b/road-signs-road-construction-city-59454043.jpg"
    image = io.imread(image_url)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Обнаружение кругов и сохранение результатов
    detect_circles(image, output_prefix="hough_circles")
    
if __name__ == '__main__':
    main()