# -*- codings: utf-8 -*-

# Form implementation generated from reading ui file 'ui_viewer.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1128, 650)
        self.listView = QtWidgets.QListView(Form)
        self.listView.setGeometry(QtCore.QRect(30, 30, 171, 31))
        self.listView.setObjectName("listView")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(210, 40, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.columnView = QtWidgets.QColumnView(Form)
        self.columnView.setGeometry(QtCore.QRect(25, 91, 1081, 531))
        self.columnView.setObjectName("columnView")
        self.textBrowser = QtWidgets.QTextBrowser(Form)
        self.textBrowser.setGeometry(QtCore.QRect(410, 10, 451, 71))
        self.textBrowser.setObjectName("textBrowser")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "Open"))