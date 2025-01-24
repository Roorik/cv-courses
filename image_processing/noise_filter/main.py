import cv2
import numpy as np

from pathlib import Path

BASE_DIR = Path(__file__).parent
img = BASE_DIR.joinpath('image.png')
res = BASE_DIR.joinpath('result')

def apply_filters(image_path, output_dir):
    # Загрузка изображения
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if image is None:
        raise FileNotFoundError("Не удалось загрузить изображение.")
    
    # низкочастотный фильтр
    low_pass = cv2.GaussianBlur(image, (15, 15), 0)
    cv2.imwrite(f'{output_dir}_low_pass.jpg', low_pass)
    
    # высокочастотный фильтр 
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # применяем Гауссово размытие для уменьшения зернистости
    blurred = cv2.GaussianBlur(gray_image, (5, 5), 0)
    high_pass = cv2.Laplacian(blurred, cv2.CV_64F)    
    
    high_pass = cv2.Laplacian(gray_image, cv2.CV_64F)
    high_pass = cv2.convertScaleAbs(high_pass)
    cv2.imwrite(f'{output_dir}_high_pass.jpg', high_pass)
    
    # нелинейный медианный фильтр
    median_filtered = cv2.medianBlur(image, 5)
    cv2.imwrite(f'{output_dir}_median_filtered.jpg', median_filtered)


if __name__ == '__main__':
    apply_filters(image_path=img, output_dir=res)