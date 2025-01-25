import cv2
import numpy as np
from skimage import io
from pathlib import Path

BASE_DIR = Path(__file__).parent
res = BASE_DIR.joinpath('outline_')

def findGreatesContour(contours):
    largest_area = 0
    largest_contour_index = -1
    i = 0
    total_contours = len(contours)
    while (i < total_contours ):
        area = cv2.contourArea(contours[i])
        if(area > largest_area):
            largest_area = area
            largest_contour_index = i
        i+=1

    return largest_area, largest_contour_index

def detectObjectContours(imageUrl, output_path):
    baseImage = io.imread(imageUrl)
    image = cv2.cvtColor(baseImage, cv2.COLOR_BGR2RGB)

    imageHSV = cv2.cvtColor(baseImage, cv2.COLOR_RGB2HSV)

    mask1 = cv2.inRange(imageHSV, (0,50,20), (5,255,255))
    mask2 = cv2.inRange(imageHSV, (175,50,20), (180,255,255))

    mask = cv2.bitwise_or(mask1, mask2)
    onlyRed = cv2.bitwise_and(image, image, mask=mask)

    kernel = np.ones((9,9),np.uint8)
    opening = cv2.morphologyEx(onlyRed, cv2.MORPH_OPEN, kernel)

    resultImage = imageHSV.copy()
    resultImage[(mask > 0)] = [0, 0, 255]

    imageRGB = cv2.cvtColor(resultImage, cv2.COLOR_HSV2BGR)

    gray = cv2.cvtColor(imageRGB, cv2.COLOR_BGR2GRAY)

    _, threshold = cv2.threshold(gray, 254, 255, cv2.THRESH_BINARY)

    counturResult = np.zeros(image.shape, dtype = np.uint8)
    copyImage = image.copy()

    contours, hierarchy = cv2.findContours(threshold,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(counturResult, contours, -1, (0, 0, 255), 3)
    cv2.drawContours(copyImage, contours, -1, (0, 0, 255), 3)

    kernel = np.ones((9,9),np.uint8)
    opening = cv2.morphologyEx(counturResult, cv2.MORPH_OPEN, kernel)

    opening = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, kernel)

    counturResult = np.zeros(image.shape, dtype = np.uint8)
    copyImage = image.copy()

    contours, hierarchy = cv2.findContours(opening,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(counturResult, contours, -1, (0, 0, 255), 3)
    cv2.drawContours(copyImage, contours, -1, (0, 0, 255), 3)


    _, index = findGreatesContour(contours)

    counturResult = np.zeros(image.shape, dtype = np.uint8)
    cv2.drawContours(counturResult, contours, index, (0, 0, 255), 3)
    
    cv2.imwrite(output_path, cv2.cvtColor(counturResult, cv2.COLOR_RGB2BGR))

    
def main():
    detectObjectContours("https://habrastorage.org/r/w1560/getpro/habr/upload_files/13a/8bb/bb5/13a8bbbb52f60bad2637a2fb6fd3c725.png", f"{res}result1.png")
    detectObjectContours("https://habrastorage.org/r/w1560/getpro/habr/upload_files/cc2/a6a/679/cc2a6a679de23ddb153a686bcde33671.png", f"{res}result2.png")

if __name__ == '__main__':
    main()