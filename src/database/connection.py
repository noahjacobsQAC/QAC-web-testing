# # -*- coding: utf-8 -*-

import logging
import sqlite3
import inspect
from typing import Dict, Optional, Union

from src.logger import logger

logger = logging.getLogger(__name__)


class DatabaseConnection:

    def __init__(self, database: Union[str, Dict]):
        self.db = database
        self.conn: Optional[sqlite3.Connection] = None

        self.connection()


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


    def connection(self):

        if isinstance(self.db, str):
            self._connectSQLite3(self.db)
        elif isinstance(self.db, Dict):
            self._connectMySQL()
        else:
            logger.critical(f"unknown databse instance passed: {type(self.db)}")

    def _connectSQLite3(self, db: str):

        logger.info(f"{db}")
        try:
            self.conn = sqlite3.connect(db, timeout=10, check_same_thread=False)
        except Exception as e:
            logger.error(f"{e}")
            logger.error(e, exc_info=True)

        cursor = None
        try:
            cursor = self.conn.cursor()
            query = "PRAGMA foreign_keys = ON;"
            cursor.execute(query)
        except Exception as e:
            logger.error(f"{e}")
            logger.error(e, exc_info=True)
        else:
            self.conn.commit()


    def _connectMySQL(self):
        raise NotImplementedError


    def isDbInitialized(self) -> bool:
        if not self.conn:
            return False
        else:
            return True
