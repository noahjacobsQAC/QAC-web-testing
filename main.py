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


import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv

from PIL import Image

import pytesseract
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


    def length(img):
        pass

    def getLengths(img):
        for y in img:
            for x in y:
                pass

    def main(self, args):
        print("in main")

    def isTable(self,img):
        filePath = r'.\\temp\\'
        #read your file
        file=f"{filePath}/{img}"
        #file=f"{filePath}/oldImg.jpg"
        #file=f"{filePath}/smallbox.png"
        #file=f"{filePath}/nottable3.png"
       # file=f"{filePath}/table5.png"
        #incorrect??? file=f"{filePath}/elements.jpg"
        # incorrect file=f"{filePath}/index.png"  
        #file=f"{filePath}/table4.png"

        try:
            img = cv2.imread(file,0)
            img.shape

            #thresholding the image to a binary image
            thresh,img_bin = cv2.threshold(img,128,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)

            #inverting the image 
            img_bin = 255-img_bin
            cv2.imwrite(f'{filePath}/table_inverted.png',img_bin)
            #Plotting the image to see the output
            plotting = plt.imshow(img_bin,cmap='gray')
            plt.show()

            # countcol(width) of kernel as 100th of total width
            kernel_len = np.array(img).shape[1]//100
            # Defining a vertical kernel to detect all vertical lines of image 
            ver_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_len))
            # Defining a horizontal kernel to detect all horizontal lines of image
            hor_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_len, 1))
            # A kernel of 2x2
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))

            #Use vertical kernel to detect and save the vertical lines in a jpg
            image_1 = cv2.erode(img_bin, ver_kernel, iterations=3)
            vertical_lines = cv2.dilate(image_1, ver_kernel, iterations=3)
            cv2.imwrite(f'{filePath}/table_vertical.jpg',vertical_lines)
            #Plot the generated image
            plotting = plt.imshow(image_1,cmap='gray')
            #plt.show()

            #Use horizontal kernel to detect and save the horizontal lines in a jpg
            image_2 = cv2.erode(img_bin, hor_kernel, iterations=3)
            horizontal_lines = cv2.dilate(image_2, hor_kernel, iterations=3)
            cv2.imwrite(f'{filePath}/table_horizontal.jpg',horizontal_lines)
            #Plot the generated image
            plotting = plt.imshow(image_2,cmap='gray')
            #plt.show()

            # Combine horizontal and vertical lines in a new third image, with both having same weight.
            img_vh = cv2.addWeighted(vertical_lines, 0.5, horizontal_lines, 0.5, 0.0)
            #Eroding and thesholding the image
            img_vh = cv2.erode(~img_vh, kernel, iterations=2)
            thresh, img_vh = cv2.threshold(img_vh,128,255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            cv2.imwrite(f'{filePath}/table_img_vh.jpg', img_vh)
            bitxor = cv2.bitwise_xor(img,img_vh)
            bitnot = cv2.bitwise_not(bitxor)
            #Plotting the generated image
            plotting = plt.imshow(bitnot,cmap='gray')
            #plt.show()

            # Detect contours for following box detection
            contours, hierarchy = cv2.findContours(img_vh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            def sort_contours(cnts, method="left-to-right"):
                # initialize the reverse flag and sort index
                reverse = False
                i = 0
                # handle if we need to sort in reverse
                if method == "right-to-left" or method == "bottom-to-top":
                    reverse = True
                # handle if we are sorting against the y-coordinate rather than
                # the x-coordinate of the bounding box
                if method == "top-to-bottom" or method == "bottom-to-top":
                    i = 1
                # construct the list of bounding boxes and sort them from top to
                # bottom
                boundingBoxes = [cv2.boundingRect(c) for c in cnts]
                (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
                key=lambda b:b[1][i], reverse=reverse))
                # return the list of sorted contours and bounding boxes
                return (cnts, boundingBoxes)

            # Sort all the contours by top to bottom.
            contours, boundingBoxes = sort_contours(contours, method="top-to-bottom")

            #Creating a list of heights for all detected boxes
            heights = [boundingBoxes[i][3] for i in range(len(boundingBoxes))]
            #print(boundingBoxes)

            #Get mean of heights
            mean = np.mean(heights)

            #Create list box to store all boxes in  
            box = []
            # Get position (x,y), width and height for every contour and show the contour on image
            lengths = [1]
            countourCount = 0
            for c in contours:
                countourCount+=1
                #print(c)
                le = len(c)
                #print(le)
                if not (le in lengths):
                    lengths.append(le)
                x, y, w, h = cv2.boundingRect(c)
                if (w<1000 and h<500):
                    image = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
                    box.append([x,y,w,h])
            #print(lengths)
            plotting = plt.imshow(image,cmap='gray')
            #plt.show()
            power = pow(int(len(lengths)*0.75), 2)
            #print(f'table {len(lengths)}  {countourCount}  {power}')
            #print(int(50*0.75)^2)
            if power < countourCount and countourCount > 12: #and len(lengths) < 100:
                #print(f'is a table {len(lengths)}  {countourCount}')
                return True
            else:
                #print(f'is not a table {len(lengths)}  {countourCount/3}')
                return False
        except Exception as e:
            print(f'{e}')
            return False

        




        '''
        im = svg2rlg(filePath + "qac.svg")
        renderPM.drawToFile(im, filePath + "qac-img.png", fmt="PNG")
        print("Converted svg")
        filePath = r'.\\temp\\' + "displayed_screenshot.jpg"
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

        print('done')

a = main()
tables = ['bloom.png','table.png', 'table2.png', 'table3.png', 'table4.png', 'table5.png']
notTables = ['New-queensu-sign-Aug31-2015-02-600.jpg', 'smallbox.png', 'oldImg.jpg', 'nottable.png', 'nottable2.png','nottable3.png']
#print(a.isTable('table.png'))
for item in tables:
    x = a.isTable(item)
    if not x:
        print(f'Yes: {x} + {item}')
    else:
        print(f'Yes: {x}')
for item in notTables:
    x = a.isTable(item)
    if x:
        print(f'No: {x} + {item}')
    else:
        print(f'No: {x}')