# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QMainWindow
from src.gui.mainwindow.ui_main import Ui_MainWindow

'''from src.gui.dashboardwidget.dashboard import DashboardWidget
from src.gui.scrapwidget.scrap import ScrapWidget
from src.gui.viewwidget.view import ViewWidget'''
from src.gui.testwidget.testui import TestWidget
import os


class MainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        try:
            os.rmdir(os.getcwd() + "\\temp")
        except:
            pass
        try:
            os.mkdir(os.getcwd() + "\\temp")
        except:
            pass
        

        self.TestWidget = TestWidget()
        self.ui.stackedWidget.insertWidget(3,self.TestWidget)
        self.ui.btn_test.clicked.connect(self.openTestWidget)
        self.show()
        '''self.dashboardWidget = DashboardWidget()
        self.scrapWidget = ScrapWidget()
        self.ViewWidget = ViewWidget()
        self.TestWidget = TestWidget()

        self.ui.stackedWidget.insertWidget(0, self.dashboardWidget)
        self.ui.stackedWidget.insertWidget(1, self.scrapWidget)
        self.ui.stackedWidget.insertWidget(2,self.ViewWidget)
        self.ui.stackedWidget.insertWidget(3,self.TestWidget)

        self.ui.btn_dashboard.clicked.connect(self.openDashoardWidget)
        self.ui.btn_scrap.clicked.connect(self.openScrapWidget)
        self.ui.btn_viewDB.clicked.connect(self.openViewWidget)
        self.ui.btn_test.clicked.connect(self.openTestWidget)

        self.ui.stackedWidget.setCurrentIndex(0)
        
        


    def openDashoardWidget(self):
        
        self.ui.stackedWidget.setCurrentIndex(0)

    def openScrapWidget(self):
        self.ui.stackedWidget.setCurrentIndex(1)
    
    def openViewWidget(self):
        self.ui.stackedWidget.setCurrentIndex(2)
'''
    def openTestWidget(self):
        self.ui.stackedWidget.setCurrentIndex(3)


    # def page_generate(self):
    #     self.ui.stackedWidget.setCurrentIndex(1)
