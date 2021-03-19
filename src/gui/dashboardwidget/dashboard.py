# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget

from src.gui.dashboardwidget.ui_dashboard import Ui_Form as Ui_DashboardWidget

class DashboardWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_DashboardWidget()
        self.ui.setupUi(self)
