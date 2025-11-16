import cv2
import math
import numpy as np

imagename = "im1.bmp"
img = cv2.imread(imagename, 0) # 0 params, for gray image
height, width = img.shape[:2]  # image height and width
print(img)  # all image pixels value in array
print(img[10, 10])  # one pixel value in 10,10 coordinate

for y in (range(height// 4)):
    for x in (range(width // 4)):
        print(img[y,x], end = "\n")
    print("\t")