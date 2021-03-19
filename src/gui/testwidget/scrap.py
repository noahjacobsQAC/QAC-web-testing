# -*- coding: utf-8 -*-

import json
import logging
from logging import error
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

        # self.ui.lineEdit_addr.setText("qaconsultants.com")
        self.ui.treeWidget_scrap.expandToDepth(0)

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

        url = self.ui.lineEdit_addr.text()
        if url[-1] == '/':
            pass
        else:
            url+='/'
        addr = "https://" + url
        addr = addr.lower()

        if not self._checkValidAddr(addr):
            return


        driver = self.ui.comboBox_driver.currentText()
        tDevice = self.ui.comboBox_targetDevice.currentText()
        navDepth = int(self.ui.spinBox_navDepth.text())
        headless = self.ui.chk_headless.isChecked()
        screenshots = self.ui.chk_screenshots.isChecked()
        config = {}
        config['headless'] = self.ui.chk_headless.isChecked()
        self.operation = OperationScrapSite("sqlite/wac.db", addr, navDepth, driver, tDevice, screenshots, configuration=config)
        self.operation.signalConsole.connect(self._consoleLog)
        self.operation.signalData.connect(self._showScrapData)
        self.operation.start()


    #
    def setUrlTotal(self, value:int=0):
        self.ui.treeWidget_scrap.topLevelItem(0).setText(1, str(value))

    def setUrlDomain(self, value:int=0):
        self.ui.treeWidget_scrap.topLevelItem(0).child(0).setText(1, str(value))

    def setUrlExternal(self, value:int=0):
        self.ui.treeWidget_scrap.topLevelItem(0).child(1).setText(1, str(value))

    def setUrlInvalid(self, value:int=0):
        self.ui.treeWidget_scrap.topLevelItem(0).child(2).setText(1, str(value))

    def setUrlErrors(self, value:int=0):
        self.ui.treeWidget_scrap.topLevelItem(0).child(3).setText(1, str(value))

    def setImagesTotal(self, value:int=0):
        self.ui.treeWidget_scrap.topLevelItem(1).setText(1, str(value))

    def setImagesScrapped(self, value:int=0):
        self.ui.treeWidget_scrap.topLevelItem(1).child(0).setText(1, str(value))

    def setImagesDownloaded(self, value:int=0):
        self.ui.treeWidget_scrap.topLevelItem(1).child(1).setText(1, str(value))

    def setImagesScreenshot(self, value:int=0):
        self.ui.treeWidget_scrap.topLevelItem(1).child(2).setText(1, str(value))

    def setImagesErrors(self, value:int=0):
        self.ui.treeWidget_scrap.topLevelItem(1).child(3).setText(1, str(value))

    def getUrlTotal(self)->int:
        return int(self.ui.treeWidget_scrap.topLevelItem(0).text(1))

    def getUrlDomain(self)->int:
        return int(self.ui.treeWidget_scrap.topLevelItem(0).child(0).text(1))

    def getUrlExternal(self)->int:
        return int(self.ui.treeWidget_scrap.topLevelItem(0).child(1).text(1))

    def getUrlInvalid(self)->int:
        return int(self.ui.treeWidget_scrap.topLevelItem(0).child(2).text(1))

    def getUrlErrors(self)->int:
        return int(self.ui.treeWidget_scrap.topLevelItem(0).child(3).text(1))

    def getImagesTotal(self)->int:
        return int(self.ui.treeWidget_scrap.topLevelItem(1).text(1))

    def getImagesScrapped(self)->int:
        return int(self.ui.treeWidget_scrap.topLevelItem(1).child(0).text(1))

    def getImagesDownloaded(self)->int:
        return int(self.ui.treeWidget_scrap.topLevelItem(1).child(1).text(1))

    def getImagesScreenshot(self)->int:
        return int(self.ui.treeWidget_scrap.topLevelItem(1).child(2).text(1))

    def getImagesErrors(self)->int:
        return int(self.ui.treeWidget_scrap.topLevelItem(1).child(3).text(1))

    def _showScrapData(self, data: Dict) -> None:
        print("data")
        print(data)
        try:
            self.setUrlTotal(data['urlTotal'])
            self.setUrlDomain(data['urlDomain'])
            self.setUrlErrors(data['urlErrors'])
            self.setUrlExternal(data['urlExternal'])
            self.setUrlInvalid(data['urlInvalid'])

            self.setImagesTotal(data['imgTotal'])
            self.setImagesDownloaded(data['imgDownloaded'])
            self.setImagesErrors(data['imgErrors'])
            self.setImagesScrapped(data['imgScrapped'])
            self.setImagesScreenshot(data['imgScreenshoted'])
        except Exception as e:
            pass