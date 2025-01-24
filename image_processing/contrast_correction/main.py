import cv2
import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path

BASE_DIR = Path(__file__).parent
img = BASE_DIR.joinpath('images.jpg')
res = BASE_DIR.joinpath('result.jpg')

def linear_contrast_correction(image_path):
    # получаем изображение в грейскейле
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError("Не удалось загрузить изображение. Проверьте путь.")

    # понижаем яркость в два раза при помощи параметра alpha
    img_half_brightness = cv2.convertScaleAbs(img, alpha=0.5, beta=0)

    # растяжение гистограммы
    x_min, x_max = np.min(img_half_brightness), np.max(img_half_brightness)
    # линейное контрастное растяжение по формуле
    img_restored = (img_half_brightness - x_min) * (255.0 / (x_max - x_min))
    img_restored = img_restored.astype(np.uint8)
    
    # выравнивание гистограммы
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    img_equalized = clahe.apply(img_restored)

    # сохраняем три результата
    # оригинал
    plt.figure(figsize=(10, 4))
    plt.subplot(1, 3, 1)
    plt.title('Original')
    plt.imshow(img, cmap='gray')
    plt.axis('off')

    # этап растяжения гистограммы
    plt.subplot(1, 3, 2)
    plt.title('Brightness Restored')
    plt.imshow(img_restored, cmap='gray')
    plt.axis('off')

    # выравненное  изображение
    plt.subplot(1, 3, 3)
    plt.title('Final')
    plt.imshow(img_equalized, cmap='gray')
    plt.axis('off')

    plt.savefig(res)

if __name__ == '__main__':
    corrected_image = linear_contrast_correction(img)