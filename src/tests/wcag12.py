



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

class wcag12(QThread):
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

    def transcribe(self, src):
        return "Welcome the cbc podcast"
        filePath = r'.\\temp\\'
        ''''
        urllib.request.urlretrieve("https://audio.clyp.it/ofnzhdem.mp3?Expires=1613586576&Signature=DVBLrnMtV45yL5sIZegppbWxh9u~8UDErq6Sm-oIPzkPEQxT62hObf~b5Yvpz9VHSN9mqe7JM7qnLxGMxqQaXgwqKdNrUjzDU~ajOsHDAlUOeyILLqP-9NdFfj7Pnk~j5m5R3-9Ea2eRkUgbz4~WFK0X5R1XIHYulseqbtNXCeM_&Key-Pair-Id=APKAJ4AMQB3XYIRCZ5PA", "thing.mp3")
        #print(filePath + "thing.mp3")
        sound = AudioSegment.from_wav(filePath + "thing.wav")
        sound.export(filePath +"transcript.wav", format="wav")'''

        r = sr.Recognizer()
        file = sr.AudioFile(filePath + "thing.wav")
        with file as source:
            audio = r.record(source)
        
        script = r.recognize_google(audio)
        
        return script

    def test(self, siteID):
        altNum  = 10
        nameNum = 8
        idNum   = 9
        ariaNum = 11
        classNum = 7
        roleNum = 16 - 2
        srcNum = 12
        xPathNum = 4
        audio = self.subSystemDatabase.getSiteTypeData('elements', siteID, 'audio')
        #print(audio)
        #self.transcribe()
        print(audio)

        for item in audio:
            print(f'item: {item}')
            script = self.transcribe(item[srcNum])
            print("transcript done")
            errors = []
            role = item[roleNum]
            try:
                if len(item[roleNum]) <= 1:
                    role = ""
            except:
                role = ""
            try:
                if len(item[altNum]) <= 1:
                    alt = ""
            except:
                alt = ""
            try:
                if len(item[ariaNum]) <= 1:
                    aria = ""
            except:
                aria = ""
            
            if script != "":
                if not "alternative" in role:
                    alt = alt
                    try:
                        if len(alt) <= len(aria):
                            alt = item[ariaNum]
                    except:
                        if alt == None:
                            alt = aria
                    try:
                        if not len(alt) >= 2:
                            errors.append("No alt text provided")
                    except:
                        errors.append("WCAG 1.2.3 - No alt text provided. An alternative for time-based media must be provided that presents equivalent information")

                else:
                    errors.append("WCAG 1.2.3 - This element is roled as alternative media.")

            else:
                #audio has no speech
                pass
            
            words = script.split(" ")
            print(f'words: {words}')
            score = 0
            sibs = self.subSystemDatabase.getSiblings(item[4], siteID)
            for sib in sibs:
                print(f'sib: {sib}')
                for word in words:
                    if word in sib[altNum]:
                        score + 1
                    if word in sib[ariaNum]:
                        score + 1
                    #if word in text:
                        #score + 1
            length = len(words)
            if score/length <= 0.1:
                errors.append("WCAG 1.2.2 - Captions are provided for all prerecorded audio content")
            #script cut down, search for common unique words
            #if found: errors.append("No captions provided."

            #get siblings, test for unique words to see if there is a description.
            print("adding")
            print(f"errors: {errors}")
            self.subSystemDatabase.addNotesToSite('elements',"wcag12", item[4], str(errors), siteID)
            
            



            


    '''
    1.2.1 Audio-only and Video-only (Prerecorded): For prerecorded audio-only and prerecorded video-only media, the following are true, 
    except when the audio or video is a media alternative for text and is clearly labeled as such: (Level A)
    Prerecorded Audio-only: An alternative for time-based media is provided that presents equivalent information for prerecorded audio-only content.
    Prerecorded Video-only: Either an alternative for time-based media or an audio track is provided that presents equivalent information for prerecorded video-only content.
    

    - Check for text alternative for audio (not sure where it should be)
    - Find how to check for an audio replacement for video

    '''
    '''
    1.2.2 Captions (Prerecorded): Captions are provided for all prerecorded audio content in synchronized media, 
    except when the media is a media alternative for text and is clearly labeled as such. (Level A)
    
    - if its a video we can try to check for captions using screenshots to save time
    - figure out if we can and how to download audio and video clips
    - use python library to generate captions from audio
    - concerned about download time for videos, although most sites we test prob wont have many or any at all.
    '''
    '''
    1.2.3 Audio Description or Media Alternative (Prerecorded): An alternative for time-based media or audio description of the prerecorded video content is provided for synchronized media, 
    except when the media is a media alternative for text and is clearly labeled as such. (Level A)
    - Check for media-alternative label
    - Check for time stamped text or an associated audio replacement
    '''
    '''
    1.2.4 Captions (Live): Captions are provided for all live audio content in synchronized media. (Level AA)
    - I dont think this applies? we cant scrape live video/ I dont think this falls much in our use case.
    
    '''


    '''1.2.5 Audio Description (Prerecorded): Audio description is provided for all prerecorded video content in synchronized media. (Level AA)
    - Check if video has an audio discription alternative for video portions of time-based media

    '''
    
    '''
    1.2.6 Sign Language (Prerecorded): Sign language interpretation is provided for all prerecorded audio content in synchronized media. (Level AAA)
    - Maybe with some sort of image processing and screenshots we can do this.  Might not be as hard as it seems.

    '''

    '''
    1.2.7 Extended Audio Description (Prerecorded): Where pauses in foreground audio are insufficient to allow audio descriptions 
    to convey the sense of the video, extended audio description is provided for all prerecorded video content in synchronized media. (Level AAA)
    - if the video already has too much talking or other audio content, the seperate audio might have to be extended to fit video information
    '''

    '''
    1.2.8 Media Alternative (Prerecorded): An alternative for time-based media is provided for all prerecorded synchronized media and for all prerecorded video-only media. (Level AAA)
    - A non time-based media alternative - prob image or text
    '''

    '''
    1.2.9 Audio-only (Live): An alternative for time-based media that presents equivalent information for live audio-only content is provided. (Level AAA)
    - not captions, text/image alternative to content
    '''


