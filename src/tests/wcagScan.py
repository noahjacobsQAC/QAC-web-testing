from typing import Any, Deque, Dict, Iterable, List, Optional, Set, Tuple, Union

import inspect

from PyQt5.QtCore import QThread, pyqtSignal


from src.scrapper.scrap import Scrap
from src.excel.excel import Xlsx
import time

from src.database.wacdatabase import WACDatabase
import logging
import inspect
from src.logger import logger
from datetime import datetime
logger = logging.getLogger(__name__)



class wcagScan(QThread):
    signalConsole = pyqtSignal(str)
    scanSignal = pyqtSignal(str)
    signalFinished = pyqtSignal(bool)
    def __init__(
        self,
        url: str,
        filename: str,
        driver: str,
        headers: bool,
        targetDevice: Union[str, None],
        configuration: Optional[Dict] = None
    ) -> None:

        super().__init__()
        self.targetDevice = targetDevice
        self.headers = headers
        self.url = url
        self.filename = filename
        self.configuration = configuration
        self.driver = driver
        self.subSystemDatabase = WACDatabase("sqlite/database.db")
        
        

    
    def _setupScrap(self) -> bool:

        self.setupDriver()

        if not self.isDriverInitialized():
            print("driver not initialized!")
            return False

        
        return True


    def __getattribute__(self, name, *args, **kwargs):
        def make_interceptor(callble):
            def func(*args, **kwargs):
                logger.info(f"{name} {args} {kwargs}")
                return callble(*args, **kwargs)
            return func
        returned = object.__getattribute__(self, name)
        if inspect.isfunction(returned) or inspect.ismethod(returned):
            return make_interceptor(returned)
        return returned

    def checkTabbing(self):
        self.subsystem = Scrap(self.url, 0, self.driver, self.targetDevice, self.configuration, False)
        return self.subsystem.checkTabbing()
        

    def run(self):
        self.signalConsole.emit(f"Starting scan of {self.url}")
        self.subSystem = Scrap(self.url, 0, self.driver, self.targetDevice, self.configuration, False)

        paths = self.subSystem.loadXPaths(self.filename)

        if paths == False:
            self.signalConsole.emit(f"Unable to find path file.")
        else:    
            scans = self.subSystemDatabase.getScanTable()
            
            id = 0
            if len(scans) >= 1:
                for x in scans:
                    #print(f"x: {x}")
                    if x[0] > id:
                        id = x[0]
            id+=1
            
            time = datetime.now()
            dt = time.strftime("%d/%m/%Y %H:%M")
            self.subSystemDatabase.addScan(id, ".com", "Chrome", dt)
            self.signalConsole.emit(f"New scanID created: {id}")
            
            self.subSystem.openSite(self.url)
            self.signalConsole.emit(f"Chrome driver started...")
            try:
                count = int(self.subSystemDatabase.getMaxElemID()[0][0]) + 1
            except:
                count = 0
            #print(f'count: {count}')
            total = len(paths)
            completed = 0
            #self.subSystemDatabase.conn.cursor.fast_executemany = True
            elements = []
            self.scanSignal.emit(str(id))
            for item in paths[1:]:
                #print(completed)
                if not ((('header' in item) or ('svg' in item)) and self.headers):
                    #time.sleep(1)
                    #print('inside')
                    ats = self.subSystem.getAllAttributes(self.url, item)
                    #print('mid')
                    if ats['type'] != "":
                        


                        #print(ats)
                        
                        #self.subSystemDatabase.insertSiteTable(id, count, ats['type'], self.url, item, ats['alt'], ats['aria-current'], ats['aria-describedby'], ats['aria-hidden'],ats['aria-label'],ats['aria-required'],
                        #                                        ats['class'], ats['id'], ats['name'], ats['role'], ats['src'], ats['tabindex'], ats['target'],ats['title'], ats['href'], ats['text'], ats['type id'])
                        
                        elements.append((id, count, ats['type'], self.url, item, ats['alt'], ats['aria-current'], ats['aria-describedby'], ats['aria-hidden'],ats['aria-label'],ats['aria-required'],
                                                                ats['class'], ats['id'], ats['name'], ats['role'], ats['src'], ats['tabindex'], ats['target'],ats['title'], ats['href'], ats['text'],
                                                                ats['type id'], ats['scope'], ats['imgText'], ats['imgTable'], ats['imgIcon'], ats['srcset'],ats['lang'], str('html'), ats['fontSize'], ats['data-src']))
                        count+=1
                    #print('next')
                    #print(elements)
                completed+=1
                if completed == 1:
                    self.signalConsole.emit(f"First Element scanned of {total} elements.")
                if completed%(int(len(paths)/5)) == 0:
                    perc = int((completed/len(paths))*100)
                    self.signalConsole.emit(f'Completed scan of {completed}/{total} elements. {perc}%')
                    #print('before')
                    self.subSystemDatabase.insertLargeSiteTable(elements)
                    self.subSystemDatabase.conn.commit()
                    elements = []
                    #print('after')
                #print('done')
            
            ret1, ret2 = self.checkTabbing()
            print('got back')
            if len(ret1) > 0:
                err = "Tab progression respects a logical sequence. Error found in tab numbers: "
                for item in ret1:
                    err = err + f'{item},'
                self.subSystemDatabase.addNotesToSite("elements", "Rule 1", '/html', err, id)
            if len(ret2) > 0:
                err = "Each tab should have h2 element even if blank. These did not "
                for item in ret2:
                    err = err + f'{item},'
                self.subSystemDatabase.addNotesToSite("elements", "Rule 2", '/html', err, id)
            #self.subSystemDatabase.conn.cursor.fast_executemany = False
            self.signalConsole.emit(f"Scan Complete.")
            self.signalFinished.emit(True)
        

    def mapSite(self, filename):
        self.subSystem = Scrap(self.url, 0, self.driver, self.targetDevice, self.configuration, False)
        self.subSystem.getXPaths(self.url, filename)
        
    def openElem(self, xPath):
        self.subsystem = Scrap(self.url, 0, self.driver, self.targetDevice, self.configuration, False)
        self.signalConsole.emit("Opening Element")
        self.subsystem.openSite(self.url)
        self.subsystem.openWebElement(self.url, str(xPath))


    def output(self, scanID):
        errors = []
        data = self.subSystemDatabase.getSiteErrors('elements', scanID)
        '''for item in data:
            add = False
            for i in range(60):
                print(f'item: {item[i + 30]} i = {i}')
                if len(item[i + 30]) > 2:
                    add = True
            if add:
                errors.append(item)'''



        self.ws = Xlsx('errors.xlsx', "Sheet1")
        for x in data:
            self.ws.addRows(x)
        
        self.ws.set_col_widths(80)
        self.ws.saveWorkbook()