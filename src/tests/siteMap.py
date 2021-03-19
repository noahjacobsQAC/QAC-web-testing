from typing import Any, Deque, Dict, Iterable, List, Optional, Set, Tuple, Union

import inspect

from PyQt5.QtCore import QThread, pyqtSignal
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
#from src.scrapper.driver import Driver
from src.scrapper.scrap import Scrap
from src.database.wacdatabase import WACDatabase
import logging
import inspect
from src.logger import logger
from datetime import datetime
logger = logging.getLogger(__name__)



class siteMap(QThread):
    signalConsole = pyqtSignal(str)
    signalFinished = pyqtSignal(bool)
    def __init__(
        self,
        url: str,
        filename: str,
        driver: str,
        targetDevice: Union[str, None],
        configuration: Optional[Dict] = None
    ) -> None:

        super().__init__()
        self.targetDevice = targetDevice
        self.url = url
        self.configuration = configuration
        self.driver = driver
        self.filename = filename
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



    def run(self):
        self.signalConsole.emit(f"Starting map of {self.url}...")
        self.subSystem = Scrap(self.url, 0, self.driver, self.targetDevice, self.configuration, False)
        self.getXPaths(self.url, self.filename)
        self.signalConsole.emit(f"Map complete.")
        self.signalFinished.emit(True)
        
    def getXPaths(self, url, filename):
        
        if not self.subSystem._setupScrap():
            logger.critical(f"driver setup failed")
         
        self.subSystem.driver.get(url)
        #self.subSystem.driver.mana   manage().timeouts().implicitlyWait(10)
        try:
            WebDriverWait(self.subSystem.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '*'))
            )
        except:
            print("webwait failed")

        #time.sleep(5)
        '''EC.element_to_be_clickable((By.CLASS_NAME, 'playButton'))
        self.subSystem.driver.find_element(By.CLASS_NAME,"ule-onboarding-continue-button").click()
        self.subSystem.driver.find_element(By.CLASS_NAME,"playButton").click()'''
        elements = self.subSystem.driver.find_elements(By.TAG_NAME,'html')
        tags = []
        self.subSystem.driver.implicitly_wait(0.00001)
        self.subSystem.paths = []
        #self.subSystem.index = 0
        self.subSystem.paths.append('/html')
        self.trigger = True
        for x in elements:
            #print(x.get_attribute("innerHTML"))
            
            subElems = x.find_elements_by_xpath(".//*")
            self.elemSize = len(subElems)
            print(f'Final Total: {self.xPath(subElems,"/html", 1)}')


        allpaths=""
        for x in self.subSystem.paths:
            #print(x)
            #x = x.replace('[1]', '')
            #print(x)
            allpaths+= f"\n{x}"
            
        file = open(filename + ".txt",'w')
        file.write(allpaths)
        file.close()

        
        return self.subSystem.paths


    def xPath(self, elems, path, size):
        index = 0
        
        if self.trigger:
            #self.signalConsole.emit(f"Elements to map: {len(elems)}")
            self.trigger = False
        while len(elems) >= index + 1:
            if len(self.subSystem.paths)%(int(self.elemSize/20)) == 0 and index !=0:
                #print(f"Completed {index} of {len(elems)}" )
                perc = int((len(self.subSystem.paths)/self.elemSize)*100)
                self.signalConsole.emit(f"Completed {len(self.subSystem.paths)} elements.  {perc}%")
                
            i = 1
            while True:
                    if not (path +'/' + elems[index].tag_name + f'[{i}]') in self.subSystem.paths:
                        new = path + '/' + elems[index].tag_name + f'[{i}]'
                        

                        if elems[index].tag_name == 'svg':
                            clas = elems[index].get_attribute('class')
                            new = f'svg {clas}'   #f'//svg[@class="{clas}"][@viewbox="{viewbox}"]'
                            #print(str(at))
                            
                        if 'path' not in new: 
                            self.subSystem.paths.append(new)
                        #print(path + '/' + elems[index].tag_name + f'[{i}]')
                        #print(path + '/' + elems[index].tag_name + f'[{i}]                      Index: {index}')
                        break
                    else:
                        i+=1
            try:
                subElems = elems[index].find_elements_by_xpath(".//*")
            except:
                subElems = []
            subSize = self.xPath(subElems, path + '/' + elems[index].tag_name + f'[{i}]', size + 1)
            index += subSize + 1
            
        return index