# -*- coding: utf-8 -*-

import logging
import sys

from PyQt5.QtWidgets import QApplication
import sip 

from src.gui.main import MainWindow
from src.logger import logger

logger = logging.getLogger(__name__)

def main():
    try:
        app = QApplication(sys.argv)
        window = MainWindow()
        sys.exit(app.exec_())
    except Exception as e:
        logger.critical(f"{e}")
        logger.critical(e, exc_info=True)


if __name__ == "__main__":
    main()
    
        
else:
    input()
    exit(1)
