# -*- coding: utf-8 -*-

import datetime
import logging
from typing import Dict, List, Optional, Tuple, Union
import inspect

from PyQt5.QtCore import QThread, pyqtSignal, QObject
from src.database.wacdatabase import WACDatabase
from src.logger import logger
from src.scrapper.scrap import Scrap
from src.utils.hasher import createHashMD5
from dataclasses import asdict

from src.dataclass.classes import (
    nt_ScrapSetting,
    prefix_EleBtnTable,
    prefix_EleImgTable,
    prefix_EleUrlTable,
)

logger = logging.getLogger(__name__)


class OperationScrapSite(QThread):

    signalConsole = pyqtSignal(str)
    signalData = pyqtSignal(dict)
    signalTeardown = pyqtSignal(bool)

    def __init__(
        self,
        db: str,
        url: str,
        navdepth: int,
        driver: str,
        targetDevice: str,
        screenshots: bool,
        configuration: Optional[Dict] = None,
    ) -> None:

        super().__init__()

        
        self.count = 0
        self.url = url
        self.navdepth = navdepth
        self.driver = driver
        self.targetDevice = targetDevice
        self.configuration = configuration
        self.db = db
        self.screenshots = screenshots
        

        #
        self.emid: Optional[int] = None
        self.ssid: Optional[int] = None
        self.urlTable: str = ""
        self.imgTable: str = ""
        self.btnTable: str = ""

        #
        self.countUrlTotal:int = 0
        self.countUrlDomain:int = 0
        self.countUrlExternal:int = 0
        self.countUrlInvalid:int = 0
        self.countUrlErrors:int = 0
        self.countImagesTotal:int = 0
        self.countImagesScrapped:int = 0
        self.countImagesDownloaded:int = 0
        self.countImagesScreenshot:int = 0
        self.countImagesErrors:int = 0

        
        self.subSytemDatabase = WACDatabase(db)
        



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

    '''def updateData(self,data:dict):
        self.signalData.emit(data)'''

    def run(self):

        ret = self.operationWarmup()

        if ret:
            try:
                self.subSytemDatabase.conn.commit()
            except Exception as e:
                logger.error(f"{e}")
                logger.error(e, exc_info=True)
                return
            else:
                self.signalConsole.emit(f"warmup complete, scrapping now...")

        else:
            self.signalConsole.emit(f"error: warmup failed, not scrapping")
            return

        ret = self.operationInit()

        if ret:
            self.signalConsole.emit(f"scrap completed, performing post process functions")
        else:
            self.signalConsole.emit(f"error: scrap process failed!")
            return

        self.subSytemScrap.driver.close()


    def operationWarmup(self) -> bool:

        # hash key to match previous configuration entry
        hKey = createHashMD5(
            [self.url, self.driver, self.targetDevice, self.navdepth]
        )

        # get id from entry
        self.emid = self.subSytemDatabase.selectEMIDInEntry(self.url)
        flagScrapSetting = True
        print("EMID = " + str(self.emid))

        # if id in entry present, search for entries in scrap configs
        if self.emid:
            self.signalConsole.emit(f"previous entry found for {self.url}")
            ret = self.subSytemDatabase.selectAllScrapSetting(EMID=self.emid)

            # if configurations present , check for hashkey
            if ret:
                self.signalConsole.emit(f"{len(ret)} scrap entries found for {self.url}")

                for ret_ in ret:
                    r_ = nt_ScrapSetting._make(ret_)

                    if r_.HASHKEY == hKey:
                        self.signalConsole.emit(f"scrap found for current config HASHKEY:{hKey} on date:{r_.date}")

                        # if a hashkey present for same date skip
                        if r_.date == str(datetime.datetime.now().date()):
                            self.signalConsole.emit(f"choose different scrap configuration (for same date)")
                            return False
        

        # if entry not present , create new
        elif not self.emid:
            try:
                self.emid = self.subSytemDatabase.getMaxId("Entry") + 1
            except:
                self.emid = 1
            self.signalConsole.emit(f"creating new entry for {self.url}")
            flag = self.subSytemDatabase.insertInEntry(self.url, status="processing", desc="None")

            if not flag:
                self.signalConsole.emit(f"error: could not create new entry for {self.url}")
                return False

        # get id of new entry
         
        # if configuration not present create new
        if flagScrapSetting:
            self.signalConsole.emit(f"creating new scrap configuration " + str(self.emid))
            flag = self.subSytemDatabase.insertInScrapSetting(
                self.emid, hKey, self.driver, self.targetDevice, self.navdepth  #type:ignore
            )

            if not flag:
                self.signalConsole.emit(f"error: could not create new scrap configuration")
                return False

            else:
                self.signalConsole.emit(f"proceeding to create tables")
        else:
            print("not flagged")
        # get ssid for new configuration entry
        self.ssid = self.subSytemDatabase.getMaxId("ScrapSetting")

        # create table for elements
        self.signalConsole.emit(f"creating element tables entries")
        etrid = self.subSytemDatabase.getMaxId("ElementTableRef")

        if isinstance(etrid, int):
            if etrid == 0: etrid = 1
            else: etrid+=1

        else:
            self.signalConsole.emit(f"error: fetching element table id")
            return False

        # table names
        self.imgTable = prefix_EleImgTable+str(etrid)
        self.urlTable = prefix_EleUrlTable+str(etrid)
        self.btnTable = prefix_EleBtnTable+str(etrid)

        flag = self.subSytemDatabase.insertInElementTableRef(
            self.ssid,  #type:ignore
            self.urlTable, self.imgTable, self.btnTable
        )

        if not flag:
            self.signalConsole.emit(f"error: could not create table entries")
            return False

        else:
            self.signalConsole.emit(f"creating new element tables")
            
            if not self.subSytemDatabase.creatTableImg(self.imgTable):
                self.signalConsole.emit(f"error: cant creat new element table {self.imgTable}")
                return False

            if not self.subSytemDatabase.creatTableUrl(self.urlTable):
                self.signalConsole.emit(f"error: cant creat new element table {self.urlTable}")
                return False

        return True


    def operationInit(self) -> bool:
        trigger = True
        try:
            #print(self.driver)
            self.subSytemScrap = Scrap(self.url, self.navdepth, self.driver, self.targetDevice, self.configuration, self.screenshots)
            
            for linkData,\
                linkError,\
                imageData,\
                imageError,\
                urlError,\
                invalid,\
                external,\
                duplicate in self.subSytemScrap.scrapSite():

                a = 0
                #print("************************************************************************************" + str(len(imageData)))
                
                for item in imageData:
                    if trigger:
                        self.signalConsole.emit("Saving data into databases...")
                        trigger = False
                    a = item
                    imageDatas = asdict(a)
                    '''if imageDatas['image'] == None:
                        imageDatas['image'] = "Blank"'''
                    self.subSytemDatabase.insertImageTableData(self.imgTable, self.count , imageDatas['url'], imageDatas['id'], imageDatas['name'], imageDatas['src'], imageDatas['text'], imageDatas['altText'], 
                                                    imageDatas['width'], imageDatas['height'], imageDatas['x'], imageDatas['y'], str(imageDatas['displayed']), imageDatas['download'], imageDatas['image'])
                    self.count+=1
             

                self.signalData.emit(
                    {
                        "linkData":len(linkData),
                        "linkError": linkError,
                        "imageData": len(imageData),
                        "imageError": imageError,
                        "urlError": urlError,
                        "invalid": invalid,
                        "external": external,
                        "duplicate": duplicate
                    }
                )
            self.signalConsole.emit("Done Saving...")
        except Exception as e:
            logger.error(f"{e}")
            logger.error(e, exc_info=True)
            return False
        else:
            return True

    