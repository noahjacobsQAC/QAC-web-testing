



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

import speech_recognition as sr
from os import path
from pydub import AudioSegment
import urllib.request

class wcag13(QThread):
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

    def run(self, filename, url):
        print("wcag 1.3 starting")
        altNum  = 10
        nameNum = 8
        idNum   = 9
        ariaNum = 11
        classNum = 7
        roleNum = 16 - 2
        srcNum = 12
        xPathNum = 4
        errors = []
        data = self.subSystemDatabase.getSiteData('elements', filename)
        #print(data)
        func1List = []
        func3List = []
        for i in data:
            func1List.append(i[7])
            if "head" in i[xPathNum]:
                try:
                    ret = self.func2(i, roleNum)
                    if ret:
                        errors.append(ret)
                        print(ret)
                except:
                    pass
            if i[2] == 'div':
                func3List.append(i)
            #func1List.append(i[10])
            #func1List.append(i[11])
        print(func1List)
        try:
            ret = self.func1(func1List)
            if ret:
                print(ret)
                errors.append(ret)
        except:
            pass
        
        try:
            ret = self.func1(func1List)
            if ret:
                print(ret)
                errors.append(ret)
        except:
            pass
        
        


    '''
    1.3.1 Info and Relationships: Information, structure, and relationships conveyed through presentation can be programmatically determined or are available in text. (Level A)
    - uses aria landmarks.  check for patterns in aria-labels
    - role= heading for headings
    - check if theyre using aria-labeled-by (works with multiple ids) - should be used by all contol interfaces
    - use role of region to label areas of the page. (in div with aria-label or labeledby)
    - Positioning labels to maximize predictability of relationships
    -https://www.w3.org/WAI/WCAG21/Techniques/html/H43.html
    skip?
    - Using semantic elements to mark up structure - could check css colour
    - Using text to convey information that is conveyed by variations in presentation of text
    - Separating information and structure from presentation to enable different presentations

    -aria-labeledby and aria-describedby are the same?

    '''
    #uses aria landmarks.  check for patterns in aria-labels
    #check for landmark role
    def func1(self, labels):
        unique = []
        empty = 0
        total = len(labels)

        for label in labels:
            print(label)
            if label == None:
                empty+=1
            elif label == "":
                empty+=1
            elif label not in unique:
                unique.append(label)
        
        score = 0.5*(len(unique)/total) - 0.2*empty
        print(unique)
        return f'Common class name score: {score}'

    #role= heading for headings
    def func2(self, heads, rolenum):
        #heads = elements in the head
        errors = []
        for head in heads:
            if head[rolenum] != "heading":
                #errors.append({"Element": head, "error": "Not labeled as head."})
                return "head not roled as head"

     #- use role of region to label areas of the page. (in div with aria-label or labeledby)
    def func3(self, divs):
        ret = False
        for div in divs:
            ret = self.func4(div)
            if ret == True:
                return "The website does use regions"
        return "The website does not use regions"

            
            #part 2
    def func4(self, div):
        if div[14] == "region":
            '''if div['aria-labeled'] != None:
                return div['aria-labeled']
            else:
                return div['aria-labeledby']'''
            return True
        else:
            return False



#- Positioning labels to maximize predictability of relationships
    def func5(self, control):
        ret = ""
        if control["aria-labeledby"] == None:
            ret+= "Controls do not use labeledby"
        #if labelElem.isToTheLeftOf(fieldElem):
            #check if label is immediately to the left of given field,
        
    
    
            
    '''
    1.3.2 Meaningful Sequence: When the sequence in which content is presented affects its meaning, a correct reading sequence can be programmatically determined. (Level A)
    -not sure what to do
    -checking for white space
    '''
    def func6(self, string):
        count = 0
        length = len(string)
        for i in string:
            if i == " ":
                count+=1
            if i =='\n':
                count+=1
            if i == '\t':
                count+=1
        if count/length >= 0.3:
            return  "WCAG 1.3.2 - When the sequence in which content is presented affects its meaning, a correct reading sequence can be programmatically determined.  There is too much white space in this object that it triggered a warning for improper formatting."



    '''
    1.3.3 Sensory Characteristics: Instructions provided for understanding and operating content do not rely solely on sensory characteristics of components such as shape, size, visual location, orientation, or sound. (Level A)

    Note: For requirements related to color, refer to Guideline 1.4.
    - Providing textual identification of items that otherwise rely only on sensory information to be understood.
    -or, provide text instructions for elements use, make up for visual indications
'''