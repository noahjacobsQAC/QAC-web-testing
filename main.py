# -*- coding: utf-8 -*-

from src.scrapper.scrap import Scrap
import urllib.request
import wget
#from cairosvg import svg2png
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PIL import Image
from webptools import dwebp
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
import urllib.request
from webptools import dwebp, cwebp
from svglib.svglib import svg2rlg
#from svglib import svg2png as SVG
import pytesseract
import textdistance

import speech_recognition as sr
from os import path
from pydub import AudioSegment
class main():
    def convertToBinaryData(self,filename):
        #Convert digital data to binary format
            with open(filename, 'rb') as file:
                blobData = file.read()
            return blobData

    def writeTofile(self, data, filename):
        # Convert binary data to proper format and write it on Hard Disk
        with open(filename, 'wb') as file:
            file.write(data)


    def main(self, args):
        
        opener = urllib.request.URLopener()
        opener.addheader('User-Agent', "Mozilla/5.0")
        src = "https://www.bmo.com/dist/images/personal/bank-accounts/familybundle-meganav-300x250-en.jpg"
        srg = "https://bmo.com/dist/images/personal/bank-accounts/familybundle-meganav-300x250-en.jpg"
        filePath = r'.\\temp\\'
        filename, headers = opener.retrieve(src, filePath + "img.png")
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
        text = pytesseract.image_to_string(filePath + 'img.png')
        print(text)
        '''xPath = "html/div/div/audio"
        short = xPath
        while True:
            #print(short)
            try:
                x = short.index('/')
            except:
                x = -1
            if x >= 1:
                short = short[x+1:]
            else:
                break
        print(xPath[0:len(xPath)-len(short)])'''
        '''filePath = r'.\\temp\\'
        opener = urllib.request.URLopener()
        opener.addheader('User-Agent', "whatevers")
        opener.retrieve("https://audio.clyp.it/ofnzhdem.mp3?Expires=1613586576&Signature=DVBLrnMtV45yL5sIZegppbWxh9u~8UDErq6Sm-oIPzkPEQxT62hObf~b5Yvpz9VHSN9mqe7JM7qnLxGMxqQaXgwqKdNrUjzDU~ajOsHDAlUOeyILLqP-9NdFfj7Pnk~j5m5R3-9Ea2eRkUgbz4~WFK0X5R1XIHYulseqbtNXCeM_&Key-Pair-Id=APKAJ4AMQB3XYIRCZ5PA", "thing2.mp3")
        #print(filePath + "thing.mp3")
        sound = AudioSegment.from_wav(filePath + "thing.wav")
        sound.export(filePath +"transcript.wav", format="wav")
            '''
        '''print(textdistance.jaro_winkler('Search', 's'))
        filePath = r'.\\temp\\' 
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
        custom_config = r'--oem 3 --psm 11'''
        #custom_config = r'-c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyz --psm 6'
        #print(pytesseract.image_to_string(filePath + 'img.png', config=custom_config))
        #dwebp(filePath + "accessibility-testing-in-the-new-age-of-web-pages.webp", r'.\\temp\\' + "img.png", "-o")
        '''#filename, headers = opener.retrieve(src, filePath)
        dwebp(filePath + "oldimg.webp", r'.\\temp\\' + "img.png", "-o")
        print("Converted webp")
        data = self.convertToBinaryData(filePath + "img.png")
        self.writeTofile(data, filePath + "newImg.png")


        im = svg2rlg(filePath + "qac.svg")
        renderPM.drawToFile(im, filePath + "qac-img.png", fmt="PNG")
        print("Converted svg")
'''
        '''filePath = r'.\\temp\\' + "displayed_screenshot.jpg"
        pixmap = QPixmap(filePath).scaled(500,500, QtCore.Qt.KeepAspectRatio)
        filePath = r'.\\temp\\' + ""
        #urllib.request.urlretrieve("https://qaconsultants.com/wp-content/uploads/2020/12/em-7-xcog.webp", filePath + "old.webp")
        im = Image.open(r'.\\temp\\' + "old.webp").convert("RGB")
        im.save(filePath + "new.png", "png")
        opener = urllib.request.URLopener()
        opener.addheader('User-Agent', "whatevers")
        filename, headers = opener.retrieve("https://qaconsultants.com/wp-content/uploads/2020/12/em-7-xcog.webp", filePath + "old.webp")
        dwebp(filePath + "old.webp", filePath + "new.png", "-o")'''
        #dwebp(r'.\\temp\\' + "old.webp", r'.\\temp\\' + "old.svg", "-o")
        '''ilePath = r'.\\temp\\' + "img_"
        urllib.request.urlretrieve("https://qaconsultants.com/wp-content/uploads/2020/11/QAC_Logo_25.svg", filePath + ".svg")
        im = svg2rlg(filePath + ".svg")
        renderPM.drawToFile(im, filePath + ".png", fmt="PNG")'''
        '''url = "https://qaconsultants.com/wp-content/uploads/2020/11/QAC_Logo_25.svg"
        #urllib.request.URLopener.version = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0'
        #filePath, headers = urllib.request.urlretrieve(url)
        #wget.download(url, filePath)
        opener = urllib.request.URLopener()
        opener.addheader('User-Agent', 'Mozilla/5.0')
        fileName, headers = opener.retrieve(url, filePath)
        print(fileName)
        print(headers)
        svg2png(fileName)'''
        '''o = Scrap.defaultDesktop(args.url, args.navdepth)

        for linkData,linkError,imageData,imageError,urlError,invalid,external in o.scrapSite():
            print(f"linkData {len(linkData)}")
            print(f"imageData {len(imageData)}")
            print(f"linkError {linkError}")
            print(f"imageError {imageError}")
            print(f"urlError {urlError}")
            print(f"invalid {invalid}")
            print(f"external {external}")
            print("##################")'''

a = main()
a.main([1])