# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 14:35:28 2022

@author: xiaoqingtech01
"""


import cv2, time
import numpy as np
from matplotlib import pyplot as plt

ISTEST = False
#定义形状检测函数
def ShapeDetection(img):
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)  #寻找轮廓点
    if contours:
        aim = contours[0]
        _max = 0
    else:
        return 
    for obj in contours:
        area = cv2.contourArea(obj)  #计算轮廓内区域的面积
        if area>_max:
            _max = area
            aim = obj
            
    perimeter = cv2.arcLength(aim,True)  #计算轮廓周长
    approx = cv2.approxPolyDP(aim,0.02*perimeter,True)  #获取轮廓角点坐标
    x, y, w, h = cv2.boundingRect(approx)  #获取坐标值和宽度、高度
    
    return int(x+w/2.0), int(y+h/2.0)


def getBoard(img):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)  #转灰度图
    # gray = gray[:-300,:-300]
   
    picBright = np.sum(gray)/255./368/640
    cenBright = np.sum(gray[180:190,310:320])/255./100
    if cenBright>picBright:
        gray = 255-gray
    gray = 255-gray
    
    # thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,5,3)

    # ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    # ret, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)
    thresh = np.array(gray>130,dtype=np.uint8)*255
        
    kernel = np.ones((3,3),np.uint8)
    opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel,iterations=2)
    
    dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
    ret,fore = cv2.threshold(dist_transform,0.8*dist_transform.max(),255,0)
    
    fore = np.uint8(fore)
    if ISTEST:
        hist = cv2.calcHist([gray], [0], None, [256], [0, 256]) 
        plt.plot(hist)
        cv2.imwrite('gray.jpg', gray)
        cv2.imwrite('thresh.jpg', thresh)
        cv2.imwrite('fore.jpg', fore)
        lap = cv2.Laplacian(img, cv2.CV_32F)
        laplace = cv2.convertScaleAbs(lap)
        cv2.imwrite('laplace.jpg', laplace)
    canny = cv2.Canny(fore,60,60)  #Canny算子边缘检测
    return ShapeDetection(canny)


if __name__ == '__main__':
    ISTEST = True
    path = r'..\rain_light\vedio\rain_155800.mp4'
    video_stream=cv2.VideoCapture(path)
    ret, frame = video_stream.read()
    video_stream.release()
    img = cv2.imread('img.jpg')
    time.sleep(1)
    x, y = getBoard(img)
    print(x, y)