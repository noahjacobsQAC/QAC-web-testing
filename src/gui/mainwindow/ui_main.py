# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_main.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 600)
        MainWindow.setMinimumSize(QtCore.QSize(1000, 600))
        MainWindow.setStyleSheet("background-color: rgb(45, 45, 45);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("background-color: rgb(45, 45, 45);")
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_body = QtWidgets.QFrame(self.centralwidget)
        self.frame_body.setMinimumSize(QtCore.QSize(110, 0))
        self.frame_body.setStyleSheet("alternate-background-color: rgb(245, 245, 245);")
        self.frame_body.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_body.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_body.setObjectName("frame_body")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_body)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame_left_panel = QtWidgets.QFrame(self.frame_body)
        self.frame_left_panel.setMinimumSize(QtCore.QSize(110, 0))
        self.frame_left_panel.setMaximumSize(QtCore.QSize(100, 16777215))
        self.frame_left_panel.setAutoFillBackground(False)
        self.frame_left_panel.setStyleSheet("background-color: rgb(194, 194, 194);")
        self.frame_left_panel.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_left_panel.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame_left_panel.setObjectName("frame_left_panel")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_left_panel)
        self.verticalLayout_3.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout_3.setSpacing(1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(-1, 20, -1, -1)
        self.verticalLayout_2.setSpacing(10)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.btn_dashboard = QtWidgets.QPushButton(self.frame_left_panel)
        self.btn_dashboard.setMinimumSize(QtCore.QSize(109, 0))
        self.btn_dashboard.setObjectName("btn_dashboard")
        self.verticalLayout_2.addWidget(self.btn_dashboard)
        self.btn_scrap = QtWidgets.QPushButton(self.frame_left_panel)
        self.btn_scrap.setMinimumSize(QtCore.QSize(109, 0))
        self.btn_scrap.setObjectName("btn_scrap")
        self.verticalLayout_2.addWidget(self.btn_scrap)
        self.btn_viewDB = QtWidgets.QPushButton(self.frame_left_panel)
        self.btn_viewDB.setMinimumSize(QtCore.QSize(109, 0))
        self.btn_viewDB.setObjectName("btn_viewDB")
        self.verticalLayout_2.addWidget(self.btn_viewDB)
        self.btn_test = QtWidgets.QPushButton(self.frame_left_panel)
        self.btn_test.setMinimumSize(QtCore.QSize(109, 0))
        self.btn_test.setObjectName("btn_test")
        self.verticalLayout_2.addWidget(self.btn_test)
        self.pushButton_3 = QtWidgets.QPushButton(self.frame_left_panel)
        self.pushButton_3.setEnabled(False)
        self.pushButton_3.setMinimumSize(QtCore.QSize(109, 0))
        self.pushButton_3.setText("")
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout_2.addWidget(self.pushButton_3)
        self.pushButton_2 = QtWidgets.QPushButton(self.frame_left_panel)
        self.pushButton_2.setEnabled(False)
        self.pushButton_2.setMinimumSize(QtCore.QSize(109, 0))
        self.pushButton_2.setText("")
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_2.addWidget(self.pushButton_2)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.horizontalLayout.addWidget(self.frame_left_panel, 0, QtCore.Qt.AlignTop)
        self.frame_page = QtWidgets.QFrame(self.frame_body)
        self.frame_page.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_page.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_page.setObjectName("frame_page")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_page)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.stackedWidget = QtWidgets.QStackedWidget(self.frame_page)
        self.stackedWidget.setFocusPolicy(QtCore.Qt.NoFocus)
        self.stackedWidget.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.stackedWidget.setObjectName("stackedWidget")
        self.verticalLayout_4.addWidget(self.stackedWidget)
        self.horizontalLayout.addWidget(self.frame_page)
        self.verticalLayout.addWidget(self.frame_body)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "QAC Web Accessability Testing Tool"))
        self.btn_dashboard.setText(_translate("MainWindow", "Dashboard"))
        self.btn_scrap.setText(_translate("MainWindow", "Scrap"))
        self.btn_viewDB.setText(_translate("MainWindow", "Database"))
        self.btn_test.setText(_translate("MainWindow", "Test"))

