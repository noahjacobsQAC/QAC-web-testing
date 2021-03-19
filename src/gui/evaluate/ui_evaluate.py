# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/gui/evaluate/ui/ui_evaluate.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(825, 680)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setMaximumSize(QtCore.QSize(16777215, 200))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_5.addWidget(self.label)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setSpacing(3)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_addr = QtWidgets.QLabel(self.frame)
        self.label_addr.setMinimumSize(QtCore.QSize(135, 0))
        self.label_addr.setMaximumSize(QtCore.QSize(135, 16777215))
        self.label_addr.setObjectName("label_addr")
        self.horizontalLayout_5.addWidget(self.label_addr)
        self.btn_addrPrefix = QtWidgets.QPushButton(self.frame)
        self.btn_addrPrefix.setEnabled(False)
        self.btn_addrPrefix.setMinimumSize(QtCore.QSize(132, 0))
        self.btn_addrPrefix.setMaximumSize(QtCore.QSize(132, 16777215))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.btn_addrPrefix.setFont(font)
        self.btn_addrPrefix.setStyleSheet("background-color:white;\n"
"color:rgb(0, 0, 0);")
        self.btn_addrPrefix.setObjectName("btn_addrPrefix")
        self.horizontalLayout_5.addWidget(self.btn_addrPrefix)
        self.lineEdit_addr = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_addr.setObjectName("lineEdit_addr")
        self.horizontalLayout_5.addWidget(self.lineEdit_addr)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_driver = QtWidgets.QLabel(self.frame)
        self.label_driver.setMinimumSize(QtCore.QSize(135, 0))
        self.label_driver.setMaximumSize(QtCore.QSize(135, 16777215))
        self.label_driver.setObjectName("label_driver")
        self.horizontalLayout.addWidget(self.label_driver)
        self.comboBox_driver = QtWidgets.QComboBox(self.frame)
        self.comboBox_driver.setMinimumSize(QtCore.QSize(132, 0))
        self.comboBox_driver.setMaximumSize(QtCore.QSize(132, 16777215))
        self.comboBox_driver.setObjectName("comboBox_driver")
        self.comboBox_driver.addItem("")
        self.comboBox_driver.addItem("")
        self.horizontalLayout.addWidget(self.comboBox_driver)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_targetPlatform = QtWidgets.QLabel(self.frame)
        self.label_targetPlatform.setMinimumSize(QtCore.QSize(135, 0))
        self.label_targetPlatform.setMaximumSize(QtCore.QSize(135, 16777215))
        self.label_targetPlatform.setObjectName("label_targetPlatform")
        self.horizontalLayout_2.addWidget(self.label_targetPlatform)
        self.comboBox_targetPlatform = QtWidgets.QComboBox(self.frame)
        self.comboBox_targetPlatform.setMinimumSize(QtCore.QSize(132, 0))
        self.comboBox_targetPlatform.setMaximumSize(QtCore.QSize(132, 16777215))
        self.comboBox_targetPlatform.setObjectName("comboBox_targetPlatform")
        self.comboBox_targetPlatform.addItem("")
        self.comboBox_targetPlatform.addItem("")
        self.comboBox_targetPlatform.addItem("")
        self.comboBox_targetPlatform.addItem("")
        self.horizontalLayout_2.addWidget(self.comboBox_targetPlatform)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_navDepth = QtWidgets.QLabel(self.frame)
        self.label_navDepth.setMinimumSize(QtCore.QSize(135, 0))
        self.label_navDepth.setMaximumSize(QtCore.QSize(135, 16777215))
        self.label_navDepth.setObjectName("label_navDepth")
        self.horizontalLayout_3.addWidget(self.label_navDepth)
        self.spinBox_navDepth = QtWidgets.QSpinBox(self.frame)
        self.spinBox_navDepth.setMinimumSize(QtCore.QSize(132, 0))
        self.spinBox_navDepth.setMaximumSize(QtCore.QSize(132, 16777215))
        self.spinBox_navDepth.setObjectName("spinBox_navDepth")
        self.horizontalLayout_3.addWidget(self.spinBox_navDepth)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4.addLayout(self.verticalLayout_2)
        self.textBrowser_console = QtWidgets.QTextBrowser(self.frame)
        self.textBrowser_console.setObjectName("textBrowser_console")
        self.horizontalLayout_4.addWidget(self.textBrowser_console)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_6.addLayout(self.verticalLayout_3)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setSpacing(3)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.btn_conf = QtWidgets.QPushButton(self.frame)
        self.btn_conf.setObjectName("btn_conf")
        self.verticalLayout_4.addWidget(self.btn_conf)
        self.btn_scrap = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_scrap.sizePolicy().hasHeightForWidth())
        self.btn_scrap.setSizePolicy(sizePolicy)
        self.btn_scrap.setObjectName("btn_scrap")
        self.verticalLayout_4.addWidget(self.btn_scrap)
        self.horizontalLayout_6.addLayout(self.verticalLayout_4)
        self.verticalLayout_5.addLayout(self.horizontalLayout_6)
        self.verticalLayout.addWidget(self.frame)
        self.frame_2 = QtWidgets.QFrame(Form)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout.addWidget(self.frame_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Scrap Settings"))
        self.label_addr.setText(_translate("Form", "Address"))
        self.btn_addrPrefix.setText(_translate("Form", "https://www."))
        self.label_driver.setText(_translate("Form", "Driver"))
        self.comboBox_driver.setItemText(0, _translate("Form", "Chrome"))
        self.comboBox_driver.setItemText(1, _translate("Form", "Firefox"))
        self.label_targetPlatform.setText(_translate("Form", "Target Platform"))
        self.comboBox_targetPlatform.setItemText(0, _translate("Form", "Windows"))
        self.comboBox_targetPlatform.setItemText(1, _translate("Form", "Mac OS"))
        self.comboBox_targetPlatform.setItemText(2, _translate("Form", "Android"))
        self.comboBox_targetPlatform.setItemText(3, _translate("Form", "iOS"))
        self.label_navDepth.setText(_translate("Form", "Nav Depth"))
        self.textBrowser_console.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.btn_conf.setText(_translate("Form", "Configuration"))
        self.btn_scrap.setText(_translate("Form", "Scrap"))