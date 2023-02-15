# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 11:45:56 2022

@author: xiaoqingtech01
"""

import cv2
import numpy as np

#定义形状检测函数
def ShapeDetection(img):
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)  #寻找轮廓点
    for obj in contours:
        area = cv2.contourArea(obj)  #计算轮廓内区域的面积
        if area < 100:continue
        cv2.drawContours(imgContour, obj, -1, (255, 0, 0), 4)  #绘制轮廓线
        perimeter = cv2.arcLength(obj,True)  #计算轮廓周长
        approx = cv2.approxPolyDP(obj,0.02*perimeter,True)  #获取轮廓角点坐标
        CornerNum = len(approx)   #轮廓角点的数量
        x, y, w, h = cv2.boundingRect(approx)  #获取坐标值和宽度、高度

        #轮廓对象分类
        if CornerNum ==3: objType ="triangle"
        elif CornerNum == 4:
            if w==h: objType= "Square"
            else:objType="Rectangle"
        elif CornerNum>4: objType= "Circle"
        else:objType="N"

        cv2.rectangle(imgContour,(int(x+w/2.0-150),int(y+h/2.0-150)),
                      (int(x+w/2.0+150),int(y+h/2.0+150)),(0,0,255),2)  #绘制边界框
        cv2.putText(imgContour,objType,(x+(w//2),y+(h//2)),cv2.FONT_HERSHEY_COMPLEX,0.6,(0,0,0),1)  #绘制文字

path = r'..\rain_light\pic\Z_SURF_I_IIII_20220618031340_O_AWS_WLRD-10-10\1.jpg'
img = cv2.imread(path)
imgContour = img.copy()
# cv2.rectangle(img, (0,360),(640,368),(255,255,255),-1)
# cv2.rectangle(img, (0,0),(640,18),(255,255,255),-1)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)  #转灰度图

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


imgCanny = cv2.Canny(fore,60,60)  #Canny算子边缘检测
ShapeDetection(imgCanny)  #形状检测

cv2.imshow("gray", gray)
cv2.imshow("fore", fore)
cv2.imshow("imgCanny", imgCanny)
cv2.imshow("shape Detection", imgContour)
cv2.waitKey(0)
cv2.destroyAllWindows()
