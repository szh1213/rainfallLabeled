# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'play.ui'
##
## Created by: Qt User Interface Compiler version 6.2.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QLineEdit, QMainWindow, QPushButton, QRadioButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.actionlist = QAction(MainWindow)
        self.actionlist.setObjectName(u"actionlist")
        self.actionlist.setCheckable(True)
        self.actionlist.setChecked(True)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.mainHL = QHBoxLayout(self.centralwidget)
        self.mainHL.setSpacing(15)
        self.mainHL.setObjectName(u"mainHL")
        self.VLQWidget = QWidget(self.centralwidget)
        self.VLQWidget.setObjectName(u"VLQWidget")
        self.verticalLayout = QVBoxLayout(self.VLQWidget)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.lineEdit = QLineEdit(self.VLQWidget)
        self.lineEdit.setObjectName(u"lineEdit")

        self.verticalLayout.addWidget(self.lineEdit)

        self.label = QLabel(self.VLQWidget)
        self.label.setObjectName(u"label")
        self.label.setFrameShape(QFrame.NoFrame)

        self.verticalLayout.addWidget(self.label)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.rbtNone = QRadioButton(self.VLQWidget)
        self.rbtNone.setObjectName(u"rbtNone")

        self.horizontalLayout_2.addWidget(self.rbtNone)

        self.rbtSmall = QRadioButton(self.VLQWidget)
        self.rbtSmall.setObjectName(u"rbtSmall")

        self.horizontalLayout_2.addWidget(self.rbtSmall)

        self.rbtMiddle = QRadioButton(self.VLQWidget)
        self.rbtMiddle.setObjectName(u"rbtMiddle")

        self.horizontalLayout_2.addWidget(self.rbtMiddle)

        self.rbtBig = QRadioButton(self.VLQWidget)
        self.rbtBig.setObjectName(u"rbtBig")

        self.horizontalLayout_2.addWidget(self.rbtBig)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(20, -1, 20, -1)
        self.btnLast = QPushButton(self.VLQWidget)
        self.btnLast.setObjectName(u"btnLast")
        self.btnLast.setMinimumSize(QSize(0, 30))
        self.btnLast.setMaximumSize(QSize(80, 16777215))

        self.horizontalLayout.addWidget(self.btnLast)

        self.btnPlay = QPushButton(self.VLQWidget)
        self.btnPlay.setObjectName(u"btnPlay")
        self.btnPlay.setMinimumSize(QSize(0, 30))
        self.btnPlay.setMaximumSize(QSize(80, 16777215))

        self.horizontalLayout.addWidget(self.btnPlay)

        self.btnNext = QPushButton(self.VLQWidget)
        self.btnNext.setObjectName(u"btnNext")
        self.btnNext.setMinimumSize(QSize(0, 30))
        self.btnNext.setMaximumSize(QSize(80, 16777215))

        self.horizontalLayout.addWidget(self.btnNext)

        self.btnLoop = QPushButton(self.VLQWidget)
        self.btnLoop.setObjectName(u"btnLoop")
        self.btnLoop.setMinimumSize(QSize(0, 30))
        self.btnLoop.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout.addWidget(self.btnLoop)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.mainHL.addWidget(self.VLQWidget)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionlist.setText(QCoreApplication.translate("MainWindow", u"\u6587\u4ef6\u5217\u8868", None))
        self.lineEdit.setText(QCoreApplication.translate("MainWindow", u"\u89c6\u9891\u6587\u4ef6\u5939\u5730\u5740", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.rbtNone.setText(QCoreApplication.translate("MainWindow", u"None", None))
        self.rbtSmall.setText(QCoreApplication.translate("MainWindow", u"Small", None))
        self.rbtMiddle.setText(QCoreApplication.translate("MainWindow", u"Middle", None))
        self.rbtBig.setText(QCoreApplication.translate("MainWindow", u"Big", None))
        self.btnLast.setText("")
        self.btnPlay.setText("")
        self.btnNext.setText("")
        self.btnLoop.setText("")
    # retranslateUi

