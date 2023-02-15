# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 09:53:08 2022

@author: xiaoqingtech01
"""


import cv2
import time
import numpy as np

ISTEST = False
# 定义形状检测函数


def ShapeDetection(img):
    contours, hierarchy = cv2.findContours(
        img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  # 寻找轮廓点
    if contours:
        aim = contours[0]
        _max = 0
    else:
        return
    for obj in contours:
        area = cv2.contourArea(obj)  # 计算轮廓内区域的面积
        if area > _max:
            _max = area
            aim = obj

    perimeter = cv2.arcLength(aim, True)  # 计算轮廓周长
    approx = cv2.approxPolyDP(aim, 0.02*perimeter, True)  # 获取轮廓角点坐标
    x, y, w, h = cv2.boundingRect(approx)  # 获取坐标值和宽度、高度

    return int(x+w/2.0), int(y+h/2.0)


def getBoard(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 转灰度图
    # gray = gray[:-300,:-300]

    picBright = np.sum(gray)/255./368/640
    cenBright = np.sum(gray[180:190, 310:320])/255./100
    if cenBright > picBright:
        gray = 255-gray
    gray = 255-gray

    thresh = np.array(gray > 130, dtype=np.uint8)*255

    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    ret, fore = cv2.threshold(dist_transform, 0.8*dist_transform.max(), 255, 0)

    fore = np.uint8(fore)
    if ISTEST:
        hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
        cv2.imwrite('gray.jpg', gray)
        cv2.imwrite('thresh.jpg', thresh)
        cv2.imwrite('fore.jpg', fore)
        lap = cv2.Laplacian(img, cv2.CV_32F)
        laplace = cv2.convertScaleAbs(lap)
        cv2.imwrite('laplace.jpg', laplace)
    canny = cv2.Canny(fore, 60, 60)  # Canny算子边缘检测
    return ShapeDetection(canny)


class RainFall:
    def __init__(self):
        self.open_flag = True
        self.frameCount = 0
        self.diff = []
        self.diffHis = {}
        self.old_gray = None
        self.loop = False
        self.video_stream = None

    def analyse(self, frame):
        img_show = frame.copy()
        cv2.rectangle(img_show, (self.boardx-150, self.boardy-150),
                      (self.boardx+150, self.boardy+150), (0, 255, 0), 3)
        self.img_show = cv2.resize(img_show, (522, 300))

        self.frameCount += 1
        frame = frame[self.boardy-150:self.boardy +
                      150, self.boardx-150:self.boardx+150]
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        # cv2.imshow('test',frame)
        # cv2.waitKey(10)

        diff = cv2.absdiff(self.old_gray, frame_gray)
        # diff = cv2.absdiff(cv2.GaussianBlur(old_gray, (5, 5), 0),
        #                    cv2.GaussianBlur(frame_gray, (5, 5), 0))
        self.old_gray = frame_gray.copy()
        diff[diff < 15] = 0
        num = np.sum(diff)
        self.diff.append(num)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        diff = clahe.apply(diff)
        diff = cv2.cvtColor(diff, cv2.COLOR_GRAY2RGB)
        # diff[:,:,0]=0
        # diff[:,:,2]=0
        diff = 255-diff

    def stat(self):
        number = sum(self.diff) // len(self.diff)
        if number >= 3000:
            return ('Big', number)
        elif number >= 500:
            return ('Middle', number)
        elif number >= 30:
            return ('Small', number)
        else:
            return ('None', number)

    def cal(self):
        while self.open_flag:

            ret, frame = self.video_stream.read()
            if not ret:
                if self.diff:
                    self.diff.pop(), self.diff.pop()

                self.video_stream.release()
                self.video_stream = None
                return self.stat()

            self.analyse(frame)
            self.frameCount += 1

    def rec(self, fp):
        with open('cache.mp4', 'wb')as f:
            f.write(fp.read())
        self.video_stream = cv2.VideoCapture('cache.mp4')
        ret, frame = self.video_stream.read()

        cv2.imwrite('cache.jpg', frame)
        img = cv2.imread('cache.jpg')
        tmp = getBoard(img)
        self.boardx, self.boardy = tmp
        self.boardx = min(max(150, self.boardx), frame.shape[1]-150)
        self.boardy = min(max(160, self.boardy), frame.shape[0]-150)
        _ = frame[self.boardy-150:self.boardy +
                  150, self.boardx-150:self.boardx+150]
        _ = cv2.cvtColor(_, cv2.COLOR_BGR2RGB)
        frame_gray = cv2.cvtColor(_, cv2.COLOR_RGB2GRAY)
        self.old_gray = frame_gray.copy()
        return self.cal()


if __name__ == '__main__':
    path = r'./example.mp4'
    fp = open(path, 'rb')
    model = RainFall()
    print(model.rec(fp))
