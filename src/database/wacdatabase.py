# # -*- coding: utf-8 -*-
import datetime
import inspect
import logging
from collections import defaultdict, namedtuple
from typing import Any, Dict, List, Optional, Tuple, Union

from src.database.database import Database
from src.dataclass.classes import (
    nt_ElementTableRef, 
    nt_Entry, 
    nt_ScrapSetting
)

from src.dataclass.tables import (
    TableImb,
    TableUrl,
    siteElements
)

from src.logger import logger

logger = logging.getLogger(__name__)

class WACDatabase(Database):
    def __init__(self, database: Union[str, Dict]):
        super().__init__(database)

    # def __getattribute__(self, name, *args, **kwargs):
    #     returned = object.__getattribute__(self, name)
    #     if inspect.isfunction(returned) or inspect.ismethod(returned):
    #         print(f"Calling {name} with {args} {kwargs}")
    #     return returned

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


    def selectAllInEntry(self, url: str, date: Optional[str] = None) -> Optional[List]:

        if not date:
            query = f"SELECT * FROM Entry WHERE url=?"
            flag, ret = self.execQuery(query, (url,))

        else:
            query = f"SELECT * FROM Entry WHERE url=? AND date=?"
            flag, ret = self.execQuery(
                query,
                (
                    url,
                    date,
                ),
            )

        if not flag:
            return None
        else:
            return ret

    def selectEMIDInEntry(self, url: str) -> Optional[int]:

        query = f"SELECT EMID FROM Entry WHERE url=?"
        flag, ret = self.execQuery(query, (url,))
        print("EMID in wacdatabase " + str(ret))
        if not flag:
            return None
        elif not ret:
            return None
        else:
            return ret[0][0]

    def selectAllScrapSetting(
        self, EMID: Optional[int] = None, HASHKey: Optional[str] = None
    ) -> Optional[List]:

        if HASHKey:
            query = f"SELECT * FROM ScrapSetting WHERE HASHKey=?"
            flag, ret = self.execQuery(query, (HASHKey,))

        elif EMID:
            query = f"SELECT * FROM ScrapSetting WHERE EMID=?"
            flag, ret = self.execQuery(query, (EMID,))
        else:
            return None

        if not flag:
            return None
        elif not ret:
            return None
        else:
            return ret


    def selectSSIDInScrapSetting(
        self, EMID: Optional[int] = None, HASHKey: Optional[str] = None
    ) -> Optional[int]:

        if HASHKey:
            query = f"SELECT SSID FROM ScrapSetting WHERE HASHKey=?"
            flag, ret = self.execQuery(query, (HASHKey,))

        elif EMID:
            query = f"SELECT SSID FROM ScrapSetting WHERE EMID=?"
            flag, ret = self.execQuery(query, (EMID,))
        else:
            return None

        if not flag:
            return None
        elif not ret:
            return None
        else:
            cnt  = ret[0][0]
            if not cnt : return 0
            else: return cnt


    def getDataInElementTableRef(self, TEID: int) -> Optional[nt_ElementTableRef]:

        query = f"SELECT * FROM ElementTableRef WHERE TEID=?"
        flag, ret = self.execQuery(query, (TEID,))

        if not flag:
            return None
        else:
            return ret


    def insertInEntry(self, url:str, status:str = "processing", desc:Optional[str]=None) -> bool:

        query = "INSERT INTO Entry (url, status, description) VALUES (?, ?, ?)"
        values = (url, status, desc,)
        flag, _ = self.execQuery(query, values)

        if not flag:
            return False
        else:
            return True

    def insertInScrapSetting(self,
        EMID:int, HASHKey:str, driver:str, tPlatform:str, navDepth:int, date:str=str(datetime.datetime.now().date())
        ) -> bool:

        query = "INSERT INTO ScrapSetting (EMID, HASHKEY, driver, targetPlatform, navDepth, date) VALUES (?,?,?,?,?,?)"
        values = (EMID, HASHKey, driver, tPlatform, navDepth, date,)
        flag, _ = self.execQuery(query, values)

        if not flag:
            return False
        else:
            return True

    def insertInElementTableRef(self,
        SSID: int, urlTable: str, imgTable: str, btnTable: str
        ) -> bool:

        query = "INSERT INTO ElementTableRef (SSID, UrlTable, ImgTable, BtnTable) VALUES (?,?,?,?)"
        values = (SSID, urlTable, imgTable, btnTable,)
        flag, _ = self.execQuery(query, values)

        if not flag:
            return False
        else:
            return True


    def creatTableImg(self, tableName: str)->bool:

        query = TableImb % f"{tableName}"

        flag, _ = self.execQuery(query)

        if not flag:
            return False
        else:
            return True


    def insertImageTableData(self,
        table:str, TTID:int, url:str, id:int, name:str, src:str, text:str,altText:str,width:int,height:int,x:int,y:int,displayed:str,download:str, image:str
        ) -> bool:
        #src = "replace"
        query = f"INSERT INTO {table} (TIID, url, id, name, src, text, altText, width, height, x, y, displayed, download, image) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
        values = (TTID, url, id, name, src, text, altText, width, height, x, y, displayed, download, image,)
        flag, _ = self.execQuery(query, values)
        self.conn.commit()
        if not flag:
            return False
        else:
            return True
    
    def getImageTableData(self, table):
        query = f"SELECT TIID, url, id, name, src, text, altText, width, height, x, y, displayed, download, image FROM {table}"
        flag, ret = self.execQuery(query)
        if not flag:
            return False
        else:
            return ret

    def getElementTables(self, ssid):
        query = f"SELECT ImgTable FROM ElementTableRef WHERE SSID={ssid}"
        print(query)
        flag, ret = self.execQuery(query)
        if not flag:
            return False
        else:
            return ret[0]


    def insertImgData(self,
        table:str, TTID:int, url:str, id:int, name:str, src:str, text:str,altText:str,width:int,height:int,x:int,y:int,displayed:str,download:str, image:str
        ) -> bool:

        
        #src = "replaced"
        
        
        values = (TTID, url, id, name, src, text, altText, width, height, x, y, displayed, download, image,)
        fields = ('TIID', 'url', 'id', 'name', 'src', 'text', 'altText', 'width', 'height', 'x', 'y', 'displayed', 'download', 'image')
        flag = self.insertInTable(table, fields, values)

        if not flag:
            return False
        else:
            return True


    def creatTableUrl(self, tableName: str)->bool:

        query = TableUrl % f"{tableName}"

        flag, _ = self.execQuery(query)

        if not flag:
            return False
        else:
            return True

    # noah

    def scrapsQuery(self, id:int):
        query = f"SELECT ScrapSetting.SSID, url, status, driver, targetPlatform, navDepth, date FROM ScrapSetting JOIN Entry on Entry.EMID WHERE Entry.EMID = ScrapSetting.EMID AND Entry.EMID = {id} AND ScrapSetting.HASHKEY<>'';"
        cursor = self.conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()



    def insertSiteTable(self,
        scanID, elemID, Type, url, xPath, alt, ariacurrent, ariadescribedby, ariahidden, arialabel, ariarequired, clas, id, name, role, src, tabindex, target, title, href, text, typeid
        ) -> bool:

        query = f"INSERT INTO elements (scanID, elemID, Type, url, xPath, alt, ariacurrent, ariadescribedby, ariahidden, arialabel, ariarequired, class, id, name, role, src, tabindex, target, title, href, text, typeid) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
        values = (scanID, elemID, Type, url, xPath, alt, ariacurrent, ariadescribedby, ariahidden, arialabel, ariarequired, clas, id, name, role, src, tabindex, target, title, href,text,typeid,)
        flag, _ = self.execQuery(query, values)
        #print(f'flag: {flag}')
        #self.conn.commit()
        if not flag:
            return False
        else:
            return True

    def insertLargeSiteTable(self,
        data
        ) -> bool:
        #print(data)
        cols = ['scanID', 'elemID', 'Type', 'url', 'xPath', 'alt', 'ariacurrent', 'ariadescribedby', 'ariahidden', 'arialabel', 'ariarequired','class', 'id', 'name', 'role', 'src', 'tabindex',
         'target', 'title', 'href', 'text', 'typeid']
        '''query = (f"INSERT INTO elements (scanID, elemID, Type, url, xPath, alt, ariacurrent, ariadescribedby, ariahidden, arialabel, ariarequired, " +
        f"class, id, name, role, src, tabindex, target, title, href, text, typeid) VALUES (%s,%s,%s,%s,%s,%,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
        "ON DUPLICATE KEY UPDATE VALUES(scanID) ")'''
        query = (f"INSERT INTO elements (")
        for item in cols:
            query = query + (item + ", ")
        query = query[0:len(query)-2]
        query = query + (") VALUES (")
        for item in cols:
            query = query + "%s,"
        query = query[0:len(query)-1]
        query = query + ") ON DUPLICATE KEY UPDATE"
        for item in cols:
            query = query + f" {item} = VAULES({item}),"
        query = query[0:len(query)-1]
        #print(query)
        query = f"INSERT INTO elements (scanID, elemID, Type, url, xPath, alt, ariacurrent, ariadescribedby, ariahidden, arialabel, ariarequired, class, id, name, role, src, tabindex, target, title, href, text, typeid, scope, imgText, imgTable, imgIcon, srcset, lang, innerHTML, fontSize, datasrc) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
        self.conn.executemany(query, data)
        

    def getSiteData(self, table, scanID):
        query = f"SELECT scanID, elemID, Type, url, xPath, alt, ariacurrent, ariadescribedby, ariahidden, arialabel, ariarequired, class, id, name, role, src, tabindex, target, title, href, text, typeid, scope, imgText, imgIcon, srcset, lang, innerHTML, fontSize FROM {table} WHERE scanID = '{scanID}'"
        flag, ret = self.execQuery(query)
        if not flag:
            return False
        else:
            return ret

    def getSiteErrors2(self, table, scanID):
        query = f"SELECT scanID, elemID, Type, url, xPath, alt, ariacurrent, ariadescribedby, ariahidden, arialabel, ariarequired, class, id, name, role, src, tabindex, target, title, href, text, typeid, scope, imgText, imgIcon, srcset, lang, innerHTML, fontSize FROM {table} WHERE scanID = '{scanID}'"
        query = 'SELECT scanID, elemID, Type, url, xPath,'
        for i in range(30):
            query = query + f'Rule {i + 1}, '
        query = query[0:len(query)-2] + " FROM {table} WHERE scanID = '{scanID}'"

        #print(query)
        query = f"Select * FROM {table} WHERE scanID = '{scanID}'"
        
        flag, ret = self.execQuery(query)
        #print(ret)
        if not flag:
            return False
        else:
            return ret

    def getSiteErrors(self, table, scanID):
        #query = f"SELECT * FROM {table} WHERE scanID = '{scanID}'"
        #query = 'SELECT scanID, elemID, Type, url, xPath,'
        #for i in range(30):
        #    query = query + f'Rule {i + 1}, '
        #query = query[0:len(query)-2] + " FROM {table} WHERE scanID = '{scanID}'"

        #print(query)
        query = f"Select * FROM {table} WHERE scanID = '{scanID}'"
        
        flag, ret = self.execQuery(query)
        #print(ret)
        if not flag:
            return False
        else:
            return ret

    def getSiblings(self, parent, scanID):
        query = f"SELECT elemID, scanID, type, url, xPath, nonText, decorative, class, name, id, alt, arialabel, src FROM elements WHERE parent = '{parent}' and scanID = '{scanID}'"
        flag, ret = self.execQuery(query)
        if not flag:
            return False
        else:
            return ret

    def getTypeWhereColEquals(self, col, value, scanID):
        query = f"SELECT type FROM elements WHERE '{col}' = '{value}' and scanID = '{scanID}'"
        flag, ret = self.execQuery(query)
        if not flag:
            return False
        else:
            return ret

    def getSiteTypeData(self, table, scanID, type):
        query = f"SELECT scanID, elemID, Type, url, xPath, alt, ariacurrent, ariadescribedby, ariahidden, arialabel, ariarequired, class, id, name, role, src, tabindex, target, title, href, text, typeid, scope, imgText, imgIcon, srcset, lang, innerHTML, fontSize FROM {table} WHERE scanID = '{scanID}' and type = '{type}'"
        flag, ret = self.execQuery(query)
        if not flag:
            return False
        else:
            return ret

    def getElemByClass(self, table, scanID, clas):
        query = f"SELECT scanID, elemID, Type, url, xPath, alt, ariacurrent, ariadescribedby, ariahidden, arialabel, ariarequired, class, id, name, role, src, tabindex, target, title, href,text, typeid, scope, imgText, imgIcon, srcset, lang, innerHTML, fontSize FROM {table} WHERE scanID = '{scanID}' and class = '{clas}'"
        flag, ret = self.execQuery(query)
        if not flag:
            return False
        else:
            return ret

    def getElemByXPath(self, table, scanID, xpath):
        query = f"SELECT scanID, elemID, Type, url, xPath, alt, ariacurrent, ariadescribedby, ariahidden, arialabel, ariarequired, class, id, name, role, src, tabindex, target, title, href, text, typeid, scope, imgText, imgIcon, srcset, lang, innerHTML, fontSize FROM {table} WHERE scanID = '{scanID}' and xPath = '{xpath}'"
        flag, ret = self.execQuery(query)
        if not flag:
            return False
        else:
            return ret

    def getElemByXPathContains(self, table, scanID, xpath):
        query = f"SELECT scanID, elemID, Type, url, xPath, alt, ariacurrent, ariadescribedby, ariahidden, arialabel, ariarequired, class, id, name, role, src, tabindex, target, title, href, text, typeid, scope, imgText, imgIcon, srcset, lang, innerHTML, fontSizetext FROM {table} WHERE scanID = '{scanID}' and xPath LIKE '%{xpath}%'"
        flag, ret = self.execQuery(query)
        if not flag:
            return False
        else:
            return ret
    
    def getElemByClassContains(self, table, scanID, clas):
        query = f"SELECT scanID, elemID, Type, url, xPath, alt, ariacurrent, ariadescribedby, ariahidden, arialabel, ariarequired, class, id, name, role, src, tabindex, target, title, href, text, typeid, scope, imgText, imgIcon, srcset, lang, innerHTML, fontSize FROM {table} WHERE scanID = '{scanID}' and class LIKE '%{clas}%'"
        flag, ret = self.execQuery(query)
        if not flag:
            return False
        else:
            return ret
        
    
    def getElemByElemID(self, table, scanID, elemID):
        query = f"SELECT scanID, elemID, Type, url, xPath, alt, ariacurrent, ariadescribedby, ariahidden, arialabel, ariarequired, class, id, name, role, src, tabindex, target, title, href, text, typeid, scope, imgText, imgIcon, srcset, lang, innerHTML, fontSize FROM {table} WHERE scanID = '{scanID}' and elemID = '{elemID}'"
        flag, ret = self.execQuery(query)
        if not flag:
            return False
        else:
            return ret

    def addNotesToSite(self, table, col, xpath, note, scanID):
        query = f'Update {table} Set "{col}" = "{note}" WHERE xPath="{xpath}" and scanID ="{scanID}" '
        values = (note,xpath)
        #print(query)
        flag, ret = self.execQuery(query)
        self.conn.commit()
        if not flag:
            return False
        else:
            return ret

    def createSiteTable(self, tableName: str)->bool:

        query = siteElements % f"{tableName}"

        flag, _ = self.execQuery(query)

        if not flag:
            return False
        else:
            self.conn.commit()
            return True
            
    def addScan(self, scanID, domain, browser, date):
        query = f"INSERT INTO scans (scanID, domain, browser, date) VALUES (?,?,?,?)"
        values = (scanID, domain, browser, date,)
        flag, _ = self.execQuery(query, values)
        
        if not flag:
            return False
        else:
            self.conn.commit()
            return True
            
    def getScanTable(self):
        query = "Select * From scans"
        flag, ret = self.execQuery(query)
        if not flag:
            return False
        else:
            self.conn.commit()
            return ret

    def getMaxElemID(self):
        query = "Select MAX(elemID) From elements"
        flag, ret = self.execQuery(query)
        if not flag:
            return False
        else:
            print(f"ret: {ret}")
            return ret
        