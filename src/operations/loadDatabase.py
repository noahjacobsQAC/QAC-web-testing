# -*- coding: utf-8 -*-

import datetime
import logging
from typing import Dict, List, Optional, Tuple, Union
import inspect
from src.database.wacdatabase import WACDatabase

from PyQt5.QtCore import QThread, pyqtSignal, QObject
#from src.database.wacdatabase import WACDatabase
#from src.logger import logger
import sqlite3





class OperationLoadDB(QThread):

    def __init__(self, dataBase) -> None:
        super().__init__()
        self.db = WACDatabase("sqlite/wac.db")
        
    

    def getScrapSelection(self):
        return self.db.scrapsQuery()
        

