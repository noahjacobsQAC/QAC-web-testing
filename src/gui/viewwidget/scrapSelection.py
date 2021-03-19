import json
import logging
from logging import error
from typing import Dict, Optional

from PyQt5.QtCore import pyqtSlot, QTimer
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QWidget
#from src.gui.viewwidget.ui_viewer import Ui_Form as Ui_ViewWidget
from src.gui.viewwidget.ui_scrapSelection import Ui_Dialog as Ui_ScrapSelection
from src.logger import logger
from src.database.wacdatabase import WACDatabase
from PyQt5.QtCore import pyqtSignal

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

class ScrapSelection(QWidget):
    signalScrapSelection = pyqtSignal(dict)
    def __init__(self):
        super().__init__()
        self.ui = Ui_ScrapSelection()
        self.ui.setupUi(self)
        self.db = WACDatabase("sqlite/wac.db")
        self.getSites()
        self.lastSite = None
        self.lastUrl = None

        s1,s2,s3 = 60, 80, 180
        self.ui.siteSelection.setColumnWidth(0, 40)
        self.ui.siteSelection.setColumnWidth(1, 300)
        self.ui.scrapSelection.setColumnWidth(0,s1)
        self.ui.scrapSelection.setColumnWidth(1,s3)
        self.ui.scrapSelection.setColumnWidth(2,s2-10)
        self.ui.scrapSelection.setColumnWidth(3,s2)
        self.ui.scrapSelection.setColumnWidth(4,s2)
        self.ui.scrapSelection.setColumnWidth(5,s2-10)
        self.ui.scrapSelection.setColumnWidth(6,s2)

        
        
        #self.ui.btn_chooseSite.clicked.connect(self.getScraps)
        self.ui.btn_loadScrap.clicked.connect(self.loadScrap)
        self.ui.btn_delete.clicked.connect(self.deleteScrap)
        self.ui.siteSelection.itemSelectionChanged.connect(self.getScraps)

    def loadScrap(self, rowIn = -1):
        row = int(self.ui.scrapSelection.currentRow())
        if rowIn != -1:
            row = rowIn
        if row is not None:
            scrap = self.db.getElementTables(self.ui.scrapSelection.item(row, 0).text())
            scrap = scrap[0]
            #scrap = "IMG_" + str(self.ui.scrapSelection.item(row, 0).text())
            
            ret = self.db.getImageTableData(scrap) 
            
            self.scrapData = ret
            self.signalScrapSelection.emit({"url": self.ui.checkBox_8.isChecked(), "id": self.ui.checkBox_7.isChecked(),"name": self.ui.checkBox_6.isChecked(),
                                            "src": self.ui.checkBox_5.isChecked(),"text": self.ui.checkBox_4.isChecked(),"height": self.ui.checkBox_3.isChecked(),
                                            "width": self.ui.checkBox_3.isChecked(),"x": self.ui.checkBox_2.isChecked(),"y": self.ui.checkBox_2.isChecked(),
                                            "displayed": self.ui.checkBox.isChecked()})
        self.close()

    def deleteScrap(self):
        try:
            row = int(self.ui.scrapSelection.currentRow())
            ssid = self.scraps[row][0]
            url = self.scraps[row][1]
            print("ssid = " + str(ssid))

            query = f"DELETE FROM IMG_" + str(ssid)
            flag, ret = self.db.execQuery(query)

            #query = f"DELETE FROM ElementTableRef WHERE SSID=" + str(ssid) 
            #flag, ret = self.db.execQuery(query)

            query = f"UPDATE ScrapSetting Set HASHKEY = '' WHERE SSID=" + str(ssid)
            flag, ret = self.db.execQuery(query)
        except Exception as e:
            print(e)

        self.getSites()
        #r = int(self.ui.siteSelection)
        #self.sites
        print(self.lastSite)
        flag = self.getScraps(rowIn=self.lastSite)
        if not flag:
            query = f"DELETE FROM Entry WHERE url=?"
            flag, ret = self.db.execQuery(query,(self.lastUrl,))
            self.getSites()
        self.db.conn.commit()
        
    def getSites(self):
        query = "SELECT EMID, url FROM Entry"
        (flag, ret) = self.db.execQuery(query)
        rows = 0
        self.sites = ret
        self.ui.siteSelection.setRowCount(0)
        if flag:
            for idx, i in enumerate(ret):
                self.ui.siteSelection.insertRow(rows)
                rows = rows + 1
                for idx2, j in enumerate(i):
                    self.ui.siteSelection.setItem(idx,idx2, QTableWidgetItem(str(j)))
        else:
            print("getsites flag false")
        

    def getScraps(self, rowIn = -1):
        x = int(self.ui.siteSelection.currentRow())
        
        if rowIn != -1:
            x = rowIn
        if x != -1:
            self.lastSite = x
            
        print("lastSite = " + str(self.lastSite))
        id = self.sites[x][0]
        
        if id ==-1:
            id = 1
        rows = 0
        ret = self.db.scrapsQuery(id)
        print(x)
        self.lastUrl = self.sites[x][1]
        print("lastUrl: " + str(self.lastUrl))
        self.scraps = ret
        print("getScraps: " + str(ret))
        if ret == [] and rowIn !=-1:
            return False
        self.ui.scrapSelection.setRowCount(0)
        for idx, i in enumerate(ret):
            self.ui.scrapSelection.insertRow(rows)
            rows = rows + 1
            for idx2, j in enumerate(i):
                self.ui.scrapSelection.setItem(idx,idx2, QTableWidgetItem(str(j)))
        return True


    
    

