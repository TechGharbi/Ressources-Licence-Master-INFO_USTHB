import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
imgL = cv.imread('scene1.png',0)
imgR = cv.imread('scene2.png',0)
stereo = cv.StereoBM_create(numDisparities=32,
                             blockSize=15)
#Parameters
#numDisparities  the disparity search range. 
#For each pixel algorithm will find the best disparity from 0 (default minimum 
#disparity) to numDisparities. The search range can then be shifted by changing 
#the minimum disparity.
#blockSize   the linear size of the blocks compared by the algorithm. 
#The size should be odd (as the block is centered at the current pixel). 
#Larger block size implies smoother, though less accurate disparity map. 
#Smaller block size gives more detailed disparity map, but there is higher chance 
#for algorithm to find a wrong correspondence.

disparity = stereo.compute(imgL,imgR)

plt.imshow(disparity)
#plt.imshow(disparity,'gray')
plt.show()