# -*- coding: utf-8 -*-

from typing import Any, Dict

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog
from src.gui.scrapwidget.ui_configuration import Ui_Dialog as Ui_Configuration


class ConfigurationDialog(QDialog):

    signalConfigurationDict = pyqtSignal(dict)

    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_Configuration()
        self.ui.setupUi(self)

        self.ui.btn_load.clicked.connect(self.BtnLoad)
        self._start()


    def _start(self):
        pass


    def BtnLoad(self):

        # self.signalTranslationDict.emit(self._getTreeConfiguration()) #type:ignore
        self.signalConfigurationDict.emit({"this": "is a test", "we" : {"can" : "do this too"}}) #type:ignore
        self.close()


    def _findKeyInTree(self, key):

        # model = self.ui.treeView_translation.model()
        # item = model.item(0)
        # for i in range(item.rowCount()):
        #     if key == item.child(i, 0).text():
        #         return item.child(i, 0)
        pass


    def _getTreeTranslationData(self):

        # model = self.ui.treeView_translation.model()

        # dictMaster = dict()

        # if not model:
        #     return dictMaster

        # item = model.item(0)
        # # print(item.rowCount())

        # # components
        # for i in range(item.rowCount()):
        #         component = item.child(i, 0).text()
        #         translation = item.child(i, 1).text()
        #         # if len(translation) == 0:
        #         #     translation = component
        #         dictMaster[component] = [translation,dict()]

        # # states
        # for key in dictMaster.keys():
        #     item = self._findKeyInTree(key)
        #     # print(f"{key}: {item.rowCount()}")
        #     _temp = dict()
        #     for i in range(item.rowCount()):
        #         state = item.child(i, 0).text()
        #         translation = item.child(i, 1).text()
        #         # if len(translation) == 0:
        #         #     translation = state
        #         _temp[state] = translation
        #         # print(f"state:{state} - translation:{translation}")
        #     dictMaster[key][1] = _temp

        # return dictMaster
        pass
