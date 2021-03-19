# -*- coding: utf-8 -*-

import json
import logging
from typing import Dict, Optional

from PyQt5.QtCore import pyqtSlot, QTimer
from PyQt5.QtWidgets import QWidget
from src.gui.scrapwidget.configuration import ConfigurationDialog
from src.gui.scrapwidget.ui_scrap import Ui_Form as Ui_ScrapWidget
from src.logger import logger

from src.scrapper.scrap import Scrap

from src.operations.opscrapsite import OperationScrapSite

logger = logging.getLogger(__name__)

class ScrapWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.ui = Ui_ScrapWidget()
        self.ui.setupUi(self)

        self.configuration = None
        self.operation = None
        self.typingTimer = QTimer()

        self.ui.lineEdit_addr.setText("google.com")

        self.ui.btn_scrap.clicked.connect(self.btnScrapSite)
        self.ui.btn_conf.clicked.connect(self.btnLoadConfiguration)

        # self.ui.btn_scrap.setEnabled(False)
        self.ui.lineEdit_addr.textChanged.connect(self._startTypingTimer)
        self.typingTimer.timeout.connect(self._endTypingTimer)


    def btnLoadConfiguration(self):
        self.configuration = ConfigurationDialog()
        self.configuration.signalConfigurationDict.connect(self.loadConfiguration)  #type:ignore
        self.configuration.show()


    def loadConfiguration(self, configuraitonDict: Dict):
        print(json.dumps(configuraitonDict, indent=2))


    def _startTypingTimer(self):
        self.typingTimer.start(1000)


    def _endTypingTimer(self):

        if not self.ui.lineEdit_addr.text():
            self.ui.btn_addrPrefix.setStyleSheet("background-color: white; color: black")


    def _checkValidAddr(self, a0:str) -> bool:

        if not a0:
            self.ui.btn_addrPrefix.setStyleSheet("background-color: white; color: black")
            return False
        else:
            if not Scrap.checkUrlValid(a0):
                logger.error(f"{a0} not valid url")
                self.ui.btn_addrPrefix.setStyleSheet("background-color: red; color: black")
                return False

            else:
                self.ui.btn_addrPrefix.setStyleSheet("background-color: green; color: black")
                return True


    def _consoleLog(self, msg: str):
        self.ui.textBrowser_console.append(msg)

    def btnScrapSite(self):

        addr = "https://www." + self.ui.lineEdit_addr.text()
        if not self._checkValidAddr(addr):
            return

        driver = self.ui.comboBox_driver.currentText()
        tPlatform = self.ui.comboBox_targetPlatform.currentText()
        navDepth = int(self.ui.spinBox_navDepth.text())

        self.operation = OperationScrapSite("sqlite/wac.db", addr, navDepth, driver, tPlatform)
        self.operation.signalConsole.connect(self._consoleLog)
        self.operation.start()
        


    def _updateConsole(self):
        pass
