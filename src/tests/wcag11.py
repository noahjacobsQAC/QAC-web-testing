



from typing import Any, Deque, Dict, Iterable, List, Optional, Set, Tuple, Union

import inspect

from PyQt5.QtCore import QThread, pyqtSignal

from selenium.webdriver.common.by import By
from src.scrapper.driver import Driver
from selenium.webdriver.support import expected_conditions as EC
from src.scrapper.scrap import Scrap
from selenium.webdriver.support.ui import WebDriverWait
from src.database.wacdatabase import WACDatabase
import logging
import inspect
from src.logger import logger
from datetime import datetime
logger = logging.getLogger(__name__)



class wcag11(QThread):
    signalConsole = pyqtSignal(str)
    def __init__(
        self,
        url: str,
        driver: str,
        targetDevice: Union[str, None],
        configuration: Optional[Dict] = None
    ) -> None:

        super().__init__()
        self.targetDevice = targetDevice
        self.url = url
        self.configuration = configuration
        self.driver = driver
        self.subSystemDatabase = WACDatabase("sqlite/database.db")
        
        

    
    def _setupScrap(self) -> bool:

        self.setupDriver()

        if not self.isDriverInitialized():
            print("driver not initialized!")
            return False

        
        return True

    #def run

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


    def start(self):
        self.subSystemDatabase.createSiteTable("Test")
       

    def testing(self, siteID, url):
        #self.subsystem.driver.get("https://www.jackboxgames.com/party-pack-five/")
        self.subsystem = Scrap(self.url, 0, self.driver, self.targetDevice, self.configuration, False)
        data = self.subSystemDatabase.getSiteData('elements', siteID)
        #print(data)
        #print(f"Data: {data}")
        back = self.subsystem.nonText(self.url, data)
        #print(f"Back: {back}")
        for item in back:
            #print(item["xPath"])
            self.subSystemDatabase.addNotesToSite('elements', "wcag11", item["xPath"], str(item["errors"]), siteID)
    
    def scan(self, filename):
        self.subSystem = Scrap(self.url, 0, self.driver, self.targetDevice, self.configuration, False)
        paths = self.subSystem.loadXPaths(filename)
        #print(paths)
        scans = self.subSystemDatabase.getScanTable()
        #print(scans)
        id = 0
        if len(scans) >= 1:
            for x in scans:
                id+=1
        #table = "site_" + str(id)
        #print(table)
        time = datetime.now()
        dt = time.strftime("%d/%m/%Y %H:%M")
        self.subSystemDatabase.addScan(id, ".com", "Chrome", dt)
        #self.subSystemDatabase.createSiteTable(table)
        self.subSystem.openSite(self.url)
        try:
            count = int(self.subSystemDatabase.getMaxElemID()[0][0]) + 1
        except:
            count = 0
        #print(count)
        for item in paths:
            #print(item)
            ats = self.subSystem.getAllAttributes(self.url, item)
            if ats['type'] != "":
                self.subSystemDatabase.insertSiteTable(id, count, ats['type'], self.url, item, ats['nonText'], ats['decorative'], ats['class'], ats['name'],ats['id'],ats['alt'],ats['aria-label'], ats['src'])
                self.subSystemDatabase.conn.commit()
                count+=1
        
    def nonText(self,url, data):
        altNum  = 10
        nameNum = 8
        idNum   = 9
        ariaNum = 11
        classNum = 7

        nonTextElems = ['img', 'button', 'input', 'video']
        
        elements = []
        #print(data)
        for item in data:
            
            #print(item)

            #if nonText
            if item[5] == "True":
                xPath = item[4]#.replace('[1]', '')
                #elem = self.driver.find_element_by_xpath(xPath)
                #elements.append(self.driver.find_element_by_xpath(xPath))
                elements.append({'type': item[2],'attributes': item, 'element': None, 'errors': [], 'xPath': xPath})
                #print(elements)
            #except:
                #print(f'Failed Path: {item}')
        
        #print(elements)
        for item in elements:
            #print(item)
            
            # Get name and alt text
            try:
                alt = item['attributes'][altNum]
                #print(f"alt: {alt}")
            except:
                item['errors'].append("WCAG 1.1.1 - All non-text content should have an alt text.")
                alt = "Broke"
            #print(f"alt: {alt}")
            try:
                name = item['attributes'][nameNum]
                #print(f"name: {name}")
            except:
                item['errors'].append("Non-text content should have a name. Controls Must have a name.")
                name = ""
            #item['errors'].append(f"Id: {item['attributes'][idNum]}")
            try:
                if item['type'] == "input" or item['type'] == "button":
                    aria = item['attributes'][ariaNum]
                    if not aria  == "":
                        alt = aria
                    else:
                        item['errors'].append("WCAG 1.1.1 - Control did not have an aria label to replace alt.")
                elif "captcha" in item['attributes'][classNum]:
                    item['errors'].append("WCAG 1.1.1 - Exception: Captcha not tested for alt text.")
            except:

                pass
        
            #Is displayed
            #Error not displayed - never displayed?
            
            #item['errors'].append(f"alt = {alt}")
            
            item['attributes'] = (f"Name: {name}   Alt: {alt}.  ")
            #print(item['attributes'])
            
            # Test for name and alt text
            if not len(str(alt)) >= 1:
                item['errors'].append("WCAG 1.1.1 - All non-text content should have an alt text.")

            if not len(str(name)) >= 1:
                item['errors'].append("Non-text content should have a name. Controls Must have a name.")

            # compare textdistance
            temp = textdistance.jaro_winkler(str(name).lower(), str(alt).lower())
            if temp <= .2:
                item['errors'].append(f"WCAG 1.1.1 - Name of element should match alt text or aria-label.")
        
        #print(elements)
        return elements

        '''self.ws = Xlsx('WWC.xlsx', "Sheet1")
        for x in elems:
            self.ws.addRows([x['type'], x['attributes'], x['errors']])
    
        self.ws.set_col_widths(80)
        self.ws.saveWorkbook()
        self.driver.close()'''


    def mapSite(self, filename):
        self.subSystem = Scrap(self.url, 0, self.driver, self.targetDevice, self.configuration, False)
        self.subSystem.getXPaths(self.url, filename)
        
    def openElem(self, xPath):
        self.subsystem = Scrap(self.url, 0, self.driver, self.targetDevice, self.configuration, False)
        self.signalConsole.emit("Opening Element")
        self.subsystem.openWebElement(self.url, str(xPath))
        