# -*- coding: utf-8 -*-
import logging
import inspect
import time
from typing import Any, List, Optional, Tuple, Union

from src.database.connection import DatabaseConnection
from src.logger import logger

logger = logging.getLogger(__name__)

class Database(DatabaseConnection):

    def __init__(self, database):
        super().__init__(database)

        if not self.isDbInitialized():
            logger.error(f"database connection not established")

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

    def execQuery(self, query: str, value: Tuple = None)-> Tuple[bool, Optional[Any]]:

        time.sleep(.5)
        logger.info(f"query:{query} value:{value}")

        try:
            cursor = self.conn.cursor()
            if value:
                cursor.execute(query, value)
            else:
                cursor.execute(query)

        except Exception as e:
            logger.error(f"{e}")
            logger.error(f"query: {query} values: {value}")
            logger.error(e, exc_info=True)
            return False, None

        else:
            return True, cursor.fetchall()


    def checkTableExsists(self, tableName: str) -> Optional[bool]:

        query = f"SELECT 1 from information_schema.tables WHERE table_name = (?)"
        flag, ret = self.execQuery(query, (tableName,))

        if flag:
            if ret[0][0] == 1:
                return True
            elif not ret:
                return False
        if not flag:
            return None


    def createTable(self, table: str, columns: List[str], prop: Optional[List[List[str]]]) -> bool:

        query = f"CREATE TABLE {table} ({','.join(columns)})"
        flag, _ = self.execQuery(query=query)
        return flag


    def getMaxRowCount(self, table: str) -> Optional[int]:

        query = f"SELECT COUNT(*) FROM {table}"
        flag, ret = self.execQuery(query)

        if not flag:
            return None
        else:
            cnt  = ret[0][0]
            if not cnt :
                return 0
            else:
                return cnt


    def getMaxId(self, table: str) -> Optional[int]:

        query = f"SELECT MAX (RowId) FROM {table}"
        flag, ret = self.execQuery(query)

        if not flag:
            return None
        else:
            cnt  = ret[0][0]
            if not cnt :
                return 0
            else:
                return cnt


    def getDataByRow(self, table: str, index: int, limit: int) -> Optional[List[Any]]:

        query = f"SELECT * FROM {table} LIMIT ?, ?"
        flag, ret = self.execQuery(query, (index, limit, ))

        if not flag:
            return None
        else:
            return ret


    def selectAllFromTable(self, table: str):
        
        query = f"SELECT * FROM {table}"
        flag, ret = self.execQuery(query)

        if not flag:
            return None
        else:
            return ret


    def insertInTable(self, table:str, fields:List[str], values:List[str]):

        query = f"INSERT INTO {table} () VALUES ()"
        pass


    def createTrigger(self):
        raise NotImplementedError


    def createView(self):
        raise NotImplementedError

