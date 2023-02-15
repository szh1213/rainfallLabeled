# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 14:59:47 2022

@author: xiaoqingtech01
"""

import sys
from ui_play import Ui_MainWindow as play_mainwindow
from PySide6.QtCore import (Qt)
from PySide6.QtWidgets import (QApplication, QMainWindow, QTableView, QMenu,
                               QAbstractItemView, QSplitter, QHeaderView,
                               QButtonGroup, QDockWidget)
from PySide6.QtGui import (QPainter, QPaintEvent, QImage, QPixmap, QIcon,
                           QStandardItemModel, QStandardItem, QCursor)

import numpy as np
import numpy.core._dtype_ctypes
import cv2
import time
import os
from getBoard import getBoard


def resource_path(relative_path):
    if getattr(sys, 'frozen', False):  # 是否Bundle Resource
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class MyTableView(QTableView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        # 创建QMenu信号事件
        self.customContextMenuRequested.connect(self.showMenu)
        self.contextMenu = QMenu(self)
        self.CP = self.contextMenu.addAction('复制')
        self.JQ = self.contextMenu.addAction('剪切')
        self.NT = self.contextMenu.addAction('粘贴')
        self.CP.triggered.connect(self.copy)
        self.JQ.triggered.connect(self.cut)
        self.NT.triggered.connect(self.paste)

    def del_tb_text(self):
        try:
            indexes = self.selectedIndexes()
            for index in indexes:
                row, column = index.row(), index.column()
                model = self.model()
                item = QStandardItem()
                model.setItem(row, column, item)
            self.setModel(model)
        except BaseException as e:
            print(e)
            return

    def paste_tb_text(self):
        try:
            indexes = self.selectedIndexes()
            for index in indexes:
                index = index
                break
            r, c = index.row(), index.column()
            text = QApplication.clipboard().text()
            ls = text.split('\n')
            ls1 = []
            for row in ls:
                ls1.append(row.split('\t'))
            model = self.model()
            rows = len(ls)
            columns = len(ls1[0])
            for row in range(rows):
                for column in range(columns):
                    item = QStandardItem()
                    item.setText((str(ls1[row][column])))
                    model.setItem(row + r, column + c, item)
        except Exception as e:
            print(e)
            return

    def selected_tb_text(self):
        try:
            indexes = self.selectedIndexes()  # 获取表格对象中被选中的数据索引列表
            indexes_dict = {}
            for index in indexes:  # 遍历每个单元格
                row, column = index.row(), index.column()  # 获取单元格的行号，列号
                if row in indexes_dict.keys():
                    indexes_dict[row].append(column)
                else:
                    indexes_dict[row] = [column]

            # 将数据表数据用制表符(\t)和换行符(\n)连接，使其可以复制到excel文件中
            text = ''
            for row, columns in indexes_dict.items():
                row_data = ''
                for column in columns:
                    data = self.model().item(row, column).text()
                    if row_data:
                        row_data = row_data + '\t' + data
                    else:
                        row_data = data

                if text:
                    text = text + '\n' + row_data
                else:
                    text = row_data
            return text
        except BaseException as e:
            print(e)
            return ''

    def copy(self):
        text = self.selected_tb_text()  # 获取当前表格选中的数据
        if text:
            clipboard = QApplication.clipboard()
            clipboard.setText(text)
            # pyperclip.copy(text) # 复制数据到粘贴板

    def cut(self):
        self.copy()
        self.del_tb_text()

    def paste(self):
        self.paste_tb_text()

    def showMenu(self, pos):
        # pos 鼠标位置
        # 菜单显示前,将它移动到鼠标点击的位置
        self.contextMenu.exec_(QCursor.pos())  # 在鼠标位置显示

    def keyPressEvent(self, event):  # 重写键盘监听事件
        # 监听 CTRL+C 组合键，实现复制数据到粘贴板
        if (event.key() == Qt.Key_C) and QApplication.keyboardModifiers() == Qt.ControlModifier:
            self.copy()  # 获取当前表格选中的数据
        elif (event.key() == Qt.Key_X) and QApplication.keyboardModifiers() == Qt.ControlModifier:
            self.cut()
        elif (event.key() == Qt.Key_V) and QApplication.keyboardModifiers() == Qt.ControlModifier:
            self.paste()
        else:
            super().keyPressEvent(event)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = play_mainwindow()
        self.ui.setupUi(self)
        self.ui.btnLast.setIcon(QIcon(resource_path('img/previous.png')))
        self.ui.btnNext.setIcon(QIcon(resource_path('img/next.png')))
        self.ui.btnPlay.setIcon(QIcon(resource_path('img/play2.png')))
        self.ui.btnLoop.setIcon(QIcon(resource_path('img/blocked.png')))

        self.sim = QStandardItemModel()
        self.tableView = MyTableView(self)
        self.tableView.setModel(self.sim)
        self.tableView.clicked.connect(self.clickedlist)
        # self.tableView.setMinimumWidth(100)
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # self.spliter = QSplitter(Qt.Horizontal)

        # self.spliter.addWidget(self.ui.VLQWidget)
        # self.spliter.addWidget(self.tableView)

        # self.ui.mainHL.addWidget(self.spliter)

        self.ui.lineEdit.setEnabled(True)
        self.ui.lineEdit.setText(r'Z:\rain')
        self.ui.rbtNone.clicked.connect(self.genLabel('None'))
        self.ui.rbtSmall.clicked.connect(self.genLabel('Small'))
        self.ui.rbtMiddle.clicked.connect(self.genLabel('Middle'))
        self.ui.rbtBig.clicked.connect(self.genLabel('Big'))
        self.ui.btnLast.clicked.connect(self.setLastVdo)
        self.ui.btnPlay.clicked.connect(self.on_video)
        self.ui.btnNext.clicked.connect(self.setNextVdo)
        self.ui.btnLoop.clicked.connect(self.setLoop)
        self.ui.lineEdit.returnPressed.connect(self.openDir)

        self.QBTNG = QButtonGroup()
        self.QBTNG.addButton(self.ui.rbtNone)
        self.QBTNG.addButton(self.ui.rbtSmall)
        self.QBTNG.addButton(self.ui.rbtMiddle)
        self.QBTNG.addButton(self.ui.rbtBig)

        self.open_flag = False
        self.vdos = []
        self.vdoNum = 0
        self.vdoSeed = 0
        self.boardx, self.boardy = 320, 184
        self.painter = QPainter(self)
        self.frameCount = 0
        self.diff = []
        self.diffHis = {}
        self.old_gray = None
        self.loop = False
        self.video_stream = None

        self.labelDock = QDockWidget(self.tr("文件列表"), self)
        self.labelDock.setFeatures(QDockWidget.DockWidgetFloatable |
                                   QDockWidget.DockWidgetMovable |
                                   Qt.WindowMinimizeButtonHint)
        self.labelDock.setWidget(self.tableView)
        self.addDockWidget(Qt.RightDockWidgetArea, self.labelDock)

    def on_video(self):
        if self.open_flag:
            self.ui.btnPlay.setIcon(QIcon(resource_path('img/play2.png')))
        elif self.vdos:
            self.ui.btnPlay.setIcon(QIcon(resource_path('img/pause.png')))
            if self.video_stream is None:
                self.video_stream = cv2.VideoCapture(self.vdos[self.vdoSeed])

        self.open_flag = bool(1-self.open_flag)

    def paintEvent(self, a0: QPaintEvent):
        if self.open_flag:

            ret, frame = self.video_stream.read()
            if not ret:
                if self.diff:
                    self.diff.pop(), self.diff.pop()
                self.stat()
                self.frameCount = 0
                self.diff.clear()
                self.open_flag = False
                self.ui.btnPlay.setIcon(QIcon(resource_path('img/play2.png')))

                self.video_stream.release()
                self.video_stream = None
                print(self.vdos[self.vdoSeed])
                if self.vdoSeed < self.vdoNum-1 and self.loop:
                    self.setNextVdo()
                    self.on_video()
                else:
                    self.loop = False
                    self.ui.btnLoop.setIcon(
                        QIcon(resource_path('img/blocked.png')))
                return

            self.analyse(frame)
            name = os.path.split(self.vdos[self.vdoSeed])[1]
            self.ui.label.setPixmap(QPixmap.fromImage(self.Qframe))
            text = '进度：{}/{}   当前视频：{}  frame:{}'.format(self.vdoSeed+1,
                                                         self.vdoNum, name,
                                                         self.frameCount)

            self.setWindowTitle(text)
            self.update()
            # time.sleep(0.02)

    def genLabel(self, lb):
        def fun():
            with open(self.vdos[self.vdoSeed].replace('mp4', 'txt'), 'w')as f:
                f.write(lb)
        return fun

    def setVdo(self, index):
        if not 0 <= index < self.vdoNum:
            return
        self.frameCount = 0
        self.diff.clear()

        self.QBTNG.setExclusive(False)
        for rbt in [self.ui.rbtNone, self.ui.rbtSmall,
                    self.ui.rbtMiddle, self.ui.rbtBig]:
            rbt.setChecked(False)

        self.QBTNG.setExclusive(True)

        text = '进度：{}/{}   当前视频：{}'.format(index+1, self.vdoNum,
                                           os.path.split(self.vdos[index])[1])

        self.setWindowTitle(text)

        if not self.video_stream is None:
            self.video_stream.release()
        self.video_stream = cv2.VideoCapture(self.vdos[index])
        ret, frame = self.video_stream.read()
        if not ret:
            self.setVdo(self.vdoSeed)
            ret, frame = self.video_stream.read()

        cv2.imwrite('img.jpg', frame)
        img = cv2.imread('img.jpg')
        tmp = getBoard(img)
        self.boardx, self.boardy = tmp
        self.boardx = min(max(150, self.boardx), frame.shape[1]-150)
        self.boardy = min(max(160, self.boardy), frame.shape[0]-150)
        _ = frame[self.boardy-150:self.boardy +
                  150, self.boardx-150:self.boardx+150]
        _ = cv2.cvtColor(_, cv2.COLOR_BGR2RGB)
        frame_gray = cv2.cvtColor(_, cv2.COLOR_RGB2GRAY)
        self.old_gray = frame_gray.copy()

        self.analyse(frame.copy())
        self.ui.label.setPixmap(QPixmap.fromImage(self.Qframe))
        self.ui.label.setScaledContents(True)
        self.stat()

    def setLastVdo(self):
        self.vdoSeed -= 1
        if self.vdoSeed < 0:
            self.vdoSeed = self.vdoNum - 1
        self.setVdo(self.vdoSeed)

    def setNextVdo(self):
        self.vdoSeed += 1
        if self.vdoSeed >= self.vdoNum:
            self.vdoSeed = 0
        self.setVdo(self.vdoSeed)

    def clickedlist(self, qModelIndex):
        self.vdoSeed = qModelIndex.row()
        self.setVdo(qModelIndex.row())

    def setLoop(self):
        if self.loop:
            self.ui.btnLoop.setIcon(QIcon(resource_path('img/blocked.png')))
            self.loop = False
        else:
            self.ui.btnLoop.setIcon(QIcon(resource_path('img/loop2.png')))
            self.loop = True

    def openDir(self):
        root = self.ui.lineEdit.text()
        self.vdos = []
        for a, b, c in os.walk(root):
            for vdo in c:
                if vdo.endswith('.mp4'):
                    self.vdos.append(os.path.join(a, vdo))

        name = os.path.split(self.vdos[self.vdoSeed])[1]
        self.vdoNum = len(self.vdos)
        text = '进度：{}/{}   当前视频：{}  frame:{}'.format(self.vdoSeed+1,
                                                     self.vdoNum, name,
                                                     self.frameCount)

        self.setWindowTitle(text)
        self.sim.clear()
        self.sim.setHorizontalHeaderLabels(['标签', '地址'])
        for i, p in enumerate(self.vdos):
            self.sim.appendRow([QStandardItem('None'), QStandardItem(p)])

        # self.tableView.resizeColumnsToContents()
        # self.tableView.setColumnWidth(1, 150)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.spliter.setStretchFactor(0,6)
        # self.spliter.setStretchFactor(1,4)
        # self.tableView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.tableView.setColumnWidth(0, 50)
        self.tableView.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeToContents)
        self.setVdo(0)

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
        cv2.putText(diff, str(num), (10, 25),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
        self.screen = np.hstack((self.img_show, diff))
        self.Qframe = QImage(self.screen.data, self.screen.shape[1],
                             self.screen.shape[0], self.screen.shape[1]*3,
                             QImage.Format_RGB888)

    def stat(self):
        vdo = self.vdos[self.vdoSeed]
        if vdo not in self.diffHis and len(self.diff) > 1:
            self.diffHis[vdo] = self.diff.copy()
        if vdo in self.diffHis:
            diff = self.diffHis[vdo].copy()
        else:
            return

        number = sum(self.diff) // len(self.diff)
        if number >= 3000:
            self.sim.setItem(self.vdoSeed, 0, QStandardItem('Big'))
        elif number >= 500:
            self.sim.setItem(self.vdoSeed, 0, QStandardItem('Middle'))
        elif number >= 30:
            self.sim.setItem(self.vdoSeed, 0, QStandardItem('Small'))
        else:
            self.sim.setItem(self.vdoSeed, 0, QStandardItem('None'))

        self.sim.setItem(self.vdoSeed, 0,
                         QStandardItem(str(sum(diff)//len(diff))))

        tmp = list(map(lambda x: int(x/max(diff)*300), diff))
        bar = np.zeros((300, len(diff)+20,  3), dtype=np.uint8)
        for i, n in enumerate(tmp):
            cv2.line(bar, (i+10, 300), (i+10, 300-n), (31, 119, 180))

        self.screen = np.hstack((self.img_show, bar))
        maxdiff = str(max(diff))
        cv2.putText(self.screen, maxdiff, (520-20*len(maxdiff), 25),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(self.screen, '0', (500, 290),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)

        # cv2.putText(self.screen, '0', (500, 255),
        #             cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
        self.Qframe = QImage(self.screen.data, self.screen.shape[1],
                             self.screen.shape[0], self.screen.shape[1]*3,
                             QImage.Format_RGB888)

        self.ui.label.setPixmap(QPixmap.fromImage(self.Qframe))
        self.update()


if __name__ == '__main__':
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    window = MainWindow()
    window.setStyleSheet(open(resource_path('qss/macOS.qss')).read())
    window.setWindowIcon(QIcon(resource_path('img/logo.ico')))
    window.resize(650, 400)
    window.show()
    window.setWindowTitle('降雨视频分类')
    # window.showMaximized()
    # window.setVisible(False)
    sys.exit(app.exec())
