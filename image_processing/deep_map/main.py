import cv2
import numpy as np
from pathlib import Path
from matplotlib import pyplot

BASE_DIR = Path(__file__).parent

imgL = cv2.imread(BASE_DIR.joinpath('pics', 'photoL.jpg'))
imgR = cv2.imread(BASE_DIR.joinpath('pics', 'photoR.jpg'))

gray_left = cv2.cvtColor(imgL, cv2.COLOR_BGR2GRAY)
gray_right = cv2.cvtColor(imgR, cv2.COLOR_BGR2GRAY)

min_disp = 16
num_disp = 192 - min_disp

stereo = cv2.StereoSGBM_create(
    minDisparity=min_disp,
    numDisparities=num_disp,
    blockSize=5,
    P1=8 * 3 * 5 ** 2, 
    P2=32 * 3 * 5 ** 2,
    disp12MaxDiff=1,
    uniquenessRatio=10,
    speckleWindowSize=100,
    speckleRange=32  
)
disparity = stereo.compute(gray_left, gray_right).astype(np.float32) / 16.0

depth_map = cv2.normalize(disparity, disparity, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
depth_map = np.uint8(depth_map)

cv2.imwrite(BASE_DIR.joinpath('good_result.jpg'), depth_map)

cv2.imshow('Depth Map', depth_map)
cv2.waitKey(0)
cv2.destroyAllWindows()