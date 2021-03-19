# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_viewer.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


import json
import logging
from logging import error
from typing import Dict, Optional

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QWidget, QMainWindow, QLabel
from src.gui.viewwidget.ui_viewer import Ui_Form as Ui_ViewWidget
from src.gui.viewwidget.scrapSelection import ScrapSelection, Ui_ScrapSelection
from src.logger import logger
from src.database.wacdatabase import WACDatabase

from PyQt5.QtCore import pyqtSignal

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

import base64


class TableModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])


class ViewWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.db = WACDatabase("sqlite/wac.db")
        self.ScrapSelection = ScrapSelection()
        self.ui = Ui_ViewWidget()
        self.ui.setupUi(self)
        #self.ui.scrapSelection.setModel(self.db.getScrapSelection())
        '''filePath = r'.\\temp\\displayed_screenshot.jpg'
        pixmap = QPixmap(filePath).scaled(500,500, QtCore.Qt.KeepAspectRatio)
        self.ui.lb_screenshot.setPixmap(pixmap)'''
        
        self.ui.elemData.setColumnWidth(1, 285)
        self.ui.curIdx.setText('0')
        self.ui.btn_loadScrap.clicked.connect(self.chooseScrap)
        self.ScrapSelection.signalScrapSelection.connect(self.scrapSelected)
        self.ui.btn_next.clicked.connect(self.next)
        self.ui.btn_last.clicked.connect(self.last)
        self.ui.elemSelect.currentItemChanged.connect(self.imgSelected)
        self.ui.curIdx.textChanged.connect(self.changeInd)
        #self.ui.
       

    def updateIdx(self):
        self.ui.curIdx.setText(str(self.ui.elemSelect.currentRow() + 1))

    def last(self):
        x = self.ui.elemSelect.currentRow()
        try:
            self.ui.elemSelect.selectRow(x-1)
            
        except:
            pass

    def next(self):
        x = self.ui.elemSelect.currentRow()
        try:
            self.ui.elemSelect.selectRow(x+1)
            
        except:
            pass

    def changeInd(self):
        idx = self.ui.curIdx.text()
        
        
        try:
            self.ui.elemSelect.selectRow(int(idx) - 1)
            
        except:
            pass


    def chooseScrap(self):
        self.ScrapSelection.getSites()
        self.ScrapSelection.show()

    def scrapSelected(self, cols):
        self.ui.elemSelect.setRowCount(0)
        ret = self.ScrapSelection.scrapData
        rows = 0
        for idx, i in enumerate(ret):
            self.ui.elemSelect.insertRow(rows)
            rows = rows + 1
            self.ui.elemSelect.setItem(idx,0, QTableWidgetItem("Image"))
            self.ui.elemSelect.setItem(idx,1, QTableWidgetItem(str(rows)))
        self.ui.lb_total.setText(f"of {len(ret):02d}")

      

    def imgSelected(self):
        self.ui.curIdx.setText(str(self.ui.elemSelect.currentRow() + 1))
        #self.ui.curIdx.setText(self.ui.elemSelect.currentRow)
        self.ui.elemData.setRowCount(0)
        set = self.ui.elemSelect.currentRow()
        imgList = ["TIID", "url", "id", "name", "src","text","altText","width","height","x","y","displayed","Notes"]
        try:
            rows = 0
            for idx, i in enumerate(self.ScrapSelection.scrapData[set]):
                if len(str(i)) <= 1000:
                    self.ui.elemData.insertRow(rows)
                    
                    rows = rows + 1
                    
                    self.ui.elemData.setItem(idx,0, QTableWidgetItem(str(imgList[idx])))
                    self.ui.elemData.setItem(idx,1, QTableWidgetItem(str(i)))
                    self.ui.elemData.setItem(idx,2,QTableWidgetItem(str("NA")))
        except:
            pass
        
        try:
            row = int(self.ui.elemSelect.currentRow())
            file_pathImg = r'.\\temp\\displayed_img.png'
            file_pathSrc = r'.\\temp\\displayed_screenshot.png'
            img = self.ScrapSelection.scrapData[row][13]
            src = self.ScrapSelection.scrapData[row][12]
            bytes = b''
            self.writeTofile(bytes + src, file_pathSrc)
            #print(src)
            '''with open(file_pathImg, "wb") as fh:
                    fh.write(base64.decodebytes(img))'''
            try:
                self.writeTofile(img, file_pathImg)
                print()
            except:
                print("no image")


            if src is not str:
                pixmap = QPixmap(file_pathSrc).scaled(500,500, QtCore.Qt.KeepAspectRatio)
                self.ui.lb_screenshot.setPixmap(pixmap)

            
            try:
                pixmap = QPixmap(file_pathImg).scaled(500,500, QtCore.Qt.KeepAspectRatio)
                self.ui.lb_image.setPixmap(pixmap)
            except:
                print("img was string = " + str(img))
        except:
            pass
    
    '''def imgSelected(self):
        try:
            row = int(self.ui.dataView.currentRow())
            file_pathImg = r'.\\temp\\displayed_img.jpg'
            file_pathSrc = r'.\\temp\\displayed_screenshot.jpg'
            src = self.ScrapSelection.scrapData[row][12]
            if src is not str:
                self.writeTofile(src, file_pathSrc)
                pixmap = QPixmap(file_pathSrc)#.scaled(500,500, QtCore.Qt.KeepAspectRatio)
                self.ui.lb_screenshot.setPixmap(pixmap)

            img = self.ScrapSelection.scrapData[row][13]
            try:
                self.writeTofile(img, file_pathImg)
                pixmap = QPixmap(file_pathImg).scaled(500,500, QtCore.Qt.KeepAspectRatio)
                self.ui.lb_image.setPixmap(pixmap)
            except:
                print("img was string = " + str(img))
        except:
            pass'''

      
      
    
    def writeTofile(self, data, filename):
    # Convert binary data to proper format and write it on Hard Disk
      with open(filename, 'wb') as file:
          file.write(data)
      
   


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.title = "Image Viewer"
        self.setWindowTitle(self.title)

    def newImage(self, file):
        label = QLabel(self)
        pixmap = QPixmap(file)
        label.setPixmap(pixmap)
        self.setCentralWidget(label)
        #self.resize(pixmap.width(), pixmap.height())
        