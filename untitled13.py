# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 13:38:50 2022

@author: xiaoqingtech01
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

def unevenLightCompensate(img, blockSize):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    average = np.mean(gray)

    rows_new = int(np.ceil(gray.shape[0] / blockSize))
    cols_new = int(np.ceil(gray.shape[1] / blockSize))

    blockImage = np.zeros((rows_new, cols_new), dtype=np.float32)
    for r in range(rows_new):
        for c in range(cols_new):
            rowmin = r * blockSize
            rowmax = (r + 1) * blockSize
            if (rowmax > gray.shape[0]):
                rowmax = gray.shape[0]
            colmin = c * blockSize
            colmax = (c + 1) * blockSize
            if (colmax > gray.shape[1]):
                colmax = gray.shape[1]

            imageROI = gray[rowmin:rowmax, colmin:colmax]
            temaver = np.mean(imageROI)
            blockImage[r, c] = temaver

    blockImage = blockImage - average
    blockImage2 = cv2.resize(blockImage, (gray.shape[1], gray.shape[0]), interpolation=cv2.INTER_CUBIC)
    gray2 = gray.astype(np.float32)
    dst = gray2 - blockImage2
    dst = dst.astype(np.uint8)
    dst = cv2.GaussianBlur(dst, (9,9), 0)
    dst = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)

    return dst

#读取
path = r'..\rain_light\pic\Z_SURF_I_IIII_20220623125110_O_AWS_WLRD-10-10\1.jpg'
img = cv2.imread(path)
# img = unevenLightCompensate(img,32)
img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
ishow = img.copy()
#二值化
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
picBright = np.sum(gray)/255./368/640
cenBright = np.sum(gray[180:190,310:320])/255./100
if cenBright>picBright:
    gray = 255-gray
ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

kernel = np.ones((3,3),np.uint8)
opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel,iterations=2)

sure_bg = cv2.dilate(opening,kernel,iterations=2)
dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
ret,fore = cv2.threshold(dist_transform,0.5*dist_transform.max(),255,0)

fore = np.uint8(fore)
ret, markers = cv2.connectedComponents(fore)

plt.subplot(131)
plt.imshow(img)
plt.axis('off')
plt.subplot(132)
plt.imshow(fore)
plt.axis('off')
plt.subplot(133)
plt.imshow(markers)
plt.axis('off')
cv2.imwrite('ishow.jpg',ishow)
print(ret)

plt.show()