import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage import io
from pathlib import Path

BASE_DIR = Path(__file__).parent
res = BASE_DIR.joinpath('HSV_')

def detectColorObject(imageUrl, lower_bound, upper_bound, output_path):
    baseImage = io.imread(imageUrl)

    imageHSV = cv2.cvtColor(baseImage, cv2.COLOR_RGB2HSV)

    mask1 = cv2.inRange(imageHSV, (0,50,20), (5,255,255))
    mask2 = cv2.inRange(imageHSV, (175,50,20), (180,255,255))

    mask = cv2.bitwise_or(mask1, mask2)

    resultImage = imageHSV.copy()
    resultImage[(mask > 0)] = [0, 0, 255]
    
    resultImage = imageHSV.copy()
    resultImage[(mask > 0)] = [0, 0, 255]

    imageRGB = cv2.cvtColor(resultImage, cv2.COLOR_HSV2BGR)


    gray = cv2.cvtColor(imageRGB, cv2.COLOR_BGR2GRAY)


    _, threshold = cv2.threshold(gray, 254, 255, cv2.THRESH_BINARY)

    cv2.imwrite(output_path, cv2.cvtColor(threshold, cv2.COLOR_RGB2BGR))
    
    

def main():
    lower_red1 = (0, 50, 20)
    upper_red1 = (5, 255, 255)

    detectColorObject("https://habrastorage.org/r/w1560/getpro/habr/upload_files/13a/8bb/bb5/13a8bbbb52f60bad2637a2fb6fd3c725.png", lower_red1, upper_red1, f"{res}result1.png")
    detectColorObject("https://habrastorage.org/r/w1560/getpro/habr/upload_files/cc2/a6a/679/cc2a6a679de23ddb153a686bcde33671.png", lower_red1, upper_red1, f"{res}result2.png")


if __name__ == '__main__':
    main()