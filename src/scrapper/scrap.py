
import traceback
import os
import warnings
from collections import deque
from logging import exception, log, warning
from typing import Any, Deque, Dict, Iterable, List, Optional, Set, Tuple, Union
from urllib.parse import urlparse
import pytesseract
import requests
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By  # type:ignore
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.webdriver import WebDriver  # type:ignore
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from src.imgutils.imgutils import imgutils
from src.scrapper.driver import Driver
from src.dataclass.classes import ImageElementData, linkElementData
from src.imgutils.imgutils import imgutils
import urllib.request
from src.excel.excel import Xlsx
import time
from webptools import dwebp, cwebp
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
import shutil
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
#from fuzzywuzzy import fuzz

import logging
import inspect
from src.logger import logger
logger = logging.getLogger(__name__)

#import textdistance

class Scrap(Driver):
    def __init__(
        self, url: str, navdepth: int, driver: str, targetDevice: Union[str, None],
        configuration: Optional[Dict] = None, screenshots: bool = False
    ) -> None:

        super().__init__(webDriver=driver, targetDevice=targetDevice, configuration=configuration)
        self.url: str = url
        self.baseUrl: str = self.parseUrlBaseFromLink(url)
        self.navdepth: int = navdepth
        self.urlDepthCounter: int = 1
        self.urlVisited: Set = set()  # type:ignore
        self.urlQueue: Deque[Tuple[int, str]] = deque()
        self.img_count = 0
        self.screenshots = screenshots


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


    def _setupScrap(self) -> bool:

        self.setupDriver()

        if not self.isDriverInitialized():
            logger.critical("driver not initialized!")
            return False

        self.pushUrlQueue((self.urlDepthCounter, self.url))

        return True



    def checkTabbing(self):
        self.openSite(self.url)
        self.actions = ActionChains(self.driver)
        elem: WebElement = None
        self.actions.send_keys(Keys.TAB)
        e1Elems = []
        e2Elems = []
        elems = []
        done = False
        lastx = -100
        lasty = -100
        self.actions.perform()
        elem = self.driver.switch_to.active_element
        firstElem = elem.text
        print(firstElem)
        count = 1
        self.driver.implicitly_wait(0.05)
        while not done:
            print(done)
            
            clas = elem.get_attribute('class')
            x = elem.location['x']
            y = elem.location['y']
            try:
                elem.find_element_by_tag_name('h2')
            except:
                e2Elems.append(count)
                #elems.append(elem)
            #print(f"y: {y} lasty")
            if y < lasty:
                #print(f"y less than lasty {y}   {lasty}")
                e1Elems.append(count)
                elems.append(elem)
            
                
            elif y == lasty:
                if x < lastx:
                    e1Elems.append(count)
                    elems.append(elem)
                    #print("x is less than lastx and y equals lasty")
            lasty = y
            lastx = x
            
            #if len(elem.text) < 50:
            #    print(f"text: {elem.text} position: x={elem.location['x']}  y={elem.location['y']}")
            
            
            self.actions.perform()
            count+=1
            elem = self.driver.switch_to.active_element
            if elem.text == firstElem:
                done = True
        for elem in elems:
            imgutils.highlight_element(self.driver, elem, 'red', 3 )

        return e1Elems, e2Elems
        
            
    # def sanityCheck(self) -> bool:

    #     print(f"base url: {self.baseUrl}")
    #     print(f"url visited: {self.urlVisited}")
    #     print(f"url queue: {self.urlQueue}")
    #     print(f"nav depth: {self.navdepth}")
    #     print(f"depth counter: {self.urlDepthCounter}")
    #     print(f"queue len: {self.checkUrlQueue()}")

    #     return True
    def getNonTextElems(self, url):
        if not self._setupScrap():
            logger.critical(f"driver setup failed")
        
        self.driver.get(url)
        print("got page")
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "form"))
            )
        except:
            print("webwait failed")

        body = self.driver.find_elements(By.TAG_NAME, "body")
        html = str(body[0].get_attribute('innerHTML'))#[0:100000]
        done = False

        #print(html[0:10000])
        elements = []
        types = []
        i = 0
        nonText = []
        '''while not done:
            try:
                x1 = html.index('<')
                x2 = html.index('>')
            except:
                done = True
                break
            try:
                if html[x1 + 1] != '/':
                    elements.append({'type': None, 'attributes': None, 'notes': ""})
                    x3 = html[x1 + 1:].index(' ') + 2
                    elements[i]['type'] = html[x1 + 1:x3]
                    #print(html[x1:x3 + 10])
                    elements[i]['attributes'] = self.parseElem(html[x1:x2])

                  ###  list = ['button']
                    #print(f"'{elements[i]['type']}' ({x1},{x3}): {html[0:30]}")
                    if elements[i]['type'] not in types:
                        types.append(elements[i]['type'])
                    if "img" in elements[i]['type'] or "input" in elements[i]['type'] or "button" in elements[i]['type'] or "video" in elements[i]['type']: #and elements[i]['type'] != "form":
                        nonText.append(elements[i])
                        #print(elements[i]['attributes'])
                    
                    #print(elements[i]['type'])
                    i+=1
                    if i>=300000:
                        done = True
            except:
                pass
            
            '''
            #html = html[x2+1:]
        #print(types)
        #print(nonText)
        #print(len(nonText))
        for el in nonText:
            #print(el['type'])
            if el['type'] == "img":
                if el['attributes']['alt'] == "":
                    #print(el)
                    pass


        images = self.driver.find_elements(By.TAG_NAME, "img")
        
        passImg = []
        img_count = 0
        for image in images:
            print("checking")
            alt = image.get_attribute('alt')
            if len(alt) <= 1:
                file_path = imgutils.scrollAndScreenshotElement(self.driver, image, img_count)
                
            #id = image.get_attribute("id"),
            name = image.get_attribute("name"),
            #src = image.get_attribute("src"),
            text = image.text,
            if textdistance.jaro_winkler(alt, text) > .5:
                passImg.append([image, "text matches"])
            if textdistance.jaro_winkler(alt, id) > .5:
                passImg.append([image, "id matches"])
            if textdistance.jaro_winkler(alt, src) > .5:
                passImg.append([image, "src matches"])
            if textdistance.jaro_winkler(alt, name) > .5:
                passImg.append([image, "name matches"])
            img_count+=1 
                

            
            
    
        for x in nonText:
            if x['notes'] != 0:
                pass#print(x)
        for item in passImg:
                    print(item)

        print("Done Function")

    def spGet(self,url):
        if not self._setupScrap():
            logger.critical(f"driver setup failed")
        
        self.driver.get(url)
        print("got page")
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "form"))
            )
        except:
            print("webwait failed")






    def spencerInfoGrabber(self, url):
        

        comp = []

        art = self.driver.find_elements(By.TAG_NAME, "article")
        i = 0

        

        for x in art:
            
            if "post-3" in x.get_attribute('id') or "post-5" in x.get_attribute('id') or "post-6" in x.get_attribute('id'):
                
                html = str(x.get_attribute('innerHTML'))
                
                comp.append({'name': None, 'link': None, 'address': None, 'tags': [], 'phone': None})
                x1 = html.index("href=") 
                x2 = html[x1:].index(' ') + x1
                #print(f"x1: {x1} x2: {x2}")
                #print(html[x1-5: x2 +10])
                comp[i]['link'] = html[x1 + 6:x2-1]
                #print(comp[i]['link'])

                html = html[x2:]
                x3 = html.index('"')
                x4 = html[x3+1:].index('"') + x3+1
                comp[i]['name'] = html[x3 + 1:x4]

                try:
                    x5 = html.index("streetAddress")
                    html = html[x5:]
                    x6 = html.index('>') 
                    x7 = html[x6:].index('</') + x6
                
                    comp[i]['address'] = html[x6 + 1:x7]
                except Exception as e:
                    print(e)
                    print(html)
                

                

                #print(f"x1: {x6} x2: {x7}")
                #print(html[x6-5: x7 +10])
                try:
                    x11 = html.index("w2dc-label w2dc-label-primary w2dc-category-label")
                    x12 = html[x11:].index("&nb") + x11
                    comp[i]['tags'].append(html[x11 + 51:x12])
                except:
                    pass




                done = False
                while not done:
                    try:
                        x8 = html.index("w2dc-tag-label")
                        html = html[x8:]
                        x9 = html.index(">")
                        x10 = html[x9:].index('&') + x9
                        print(f"x8: {x8} x9: {x9}")
                        comp[i]['tags'].append(html[x9 + 1:x10])
                        html = html[x9:]

                    except Exception as e:
                        done = True
                        print(e)


                try:
                    x13 = html.index('href="tel:')
                    comp[i]['phone'] = html[x13 + 10:x13 + 22]
                except:
                    pass



                print(comp[i])






                i+=1
        self.ws = Xlsx('APMA.xlsx', "Sheet1")
        for x in comp:
            self.ws.addRows([x['name'], x['link'], x['address'], x['phone'], x['tags']])
        
        self.ws.set_col_widths(80)
        self.ws.saveWorkbook()



        self.driver.close()
        print("Function Done.")




    def parseElem(self, html) -> Tuple[str]:
        elem = {}
        #print(f"In parseElem: {html} \nParse html done")
        if not html[1]=="/":
            
            elem['Element Type'] = html[1:html.index(' ')]
            html = html[html.index(' ')-1:]
            
            while len(html)>1:
                
                point = html.index('=')
                label = html[2:point]
                html = html[point:]
                #print(html)
                point = html[2:].index('"') + 2
                if point == -1:
                    point = html.index('>')
                value = html[2:point]
                html = html[point:]
                elem[label] = value
            
            return elem
        return None


    def inputAlt(self, url):
        if not self._setupScrap():
            logger.critical(f"driver setup failed")
        
        self.driver.get(url)
        print("got page")
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "form"))
            )
        except:
            print("webwait failed")


        
       




        inputs = self.driver.find_elements(By.TAG_NAME, "form")
        #self.driver.find_elements(By.XPATH, '//button')
        print(inputs)
        print("got inputs")
        elems = {}
        for x in inputs:
            html = str(x.get_attribute('innerHTML'))
            
            x1 = html.index('<')
            x2 = html.index('>')
            
            count = 0
            while x1 != -1 and x2 != -1:
                print(f"Html split: {x1} {x2}")
                try:
                    elems[count] = self.parseElem(html[x1:x2])
                except:

                    print("couldnt parse <>")
                print("back")
                html = html[x2+2:]
                print(html)
                try:
                    x1 = html.index('<')
                    x2 = html.index('>')
                except:
                    x1 = -1

                count+=1
        paper = ""
        for x in elems:
            
            paper+= "\nNew Element: " + str(x)
            for f in elems[x]:
                paper+="\n" + str(f) + ": " + elems[x][f]

        #print(paper)    


        data: List[ImageElementData] = list()
        images = self.driver.find_elements(By.TAG_NAME, "img")
        
        for image in images:
            
            
            id = image.get_attribute("id"),
            name = image.get_attribute("name"),
            src = image.get_attribute("src"),
            text = image.text,
            alt = image.get_attribute("alt"),
            displayed = image.is_displayed(),

            if len(alt) >= 1:
                x = textdistance.jaro_winkler(alt, id)
                y = textdistance.jaro_winkler(alt, src)
                z = textdistance.jaro_winkler(alt, name)
                v = textdistance.jaro_winkler(alt, text)

                print(f"Score: {z}    - alt: {alt}  name: {name}")
                print(f"Score: {y}    - alt: {alt}  src: {src}")
                print(f"Score: {x}    - alt: {alt}  id: {id}")
                print(f"Score: {v}    - alt: {alt}  text: {text}")
            else:
                print(f"image has no alt text: {id}")
                    
                
            
        


        self.driver.close()





        print(textdistance.jaro_winkler(elems[0]['aria-label'],elems[0]['placeholder']))
        print(textdistance.jaro_winkler("Search", "Search the site"))
        print(textdistance.jaro_winkler("Search", "Chears the site"))
        print(textdistance.jaro_winkler("Sign up", "Click to sign the petition"))
        print(textdistance.jaro_winkler("Sign up", "Click to sign up the petition"))
        print(textdistance.jaro_winkler("Search", "Search the website for items"))
        print(textdistance.jaro_winkler("Search", "Search"))
        print(textdistance.jaro_winkler("Search", "Anders"))
        # You can use this over length to decide if it is good enough
        


    

    def xPath1(self, html, path, element):
        #print(f"Path: {path} Paths: {self.paths}")

        done = False
        total = 0
        while not done:
            print("Html\n" + html[0:200])
            try:
                x1 = html.index('<')
            except:
                break
            try:
                x2 = html[x1+1:].index(" ") + x1 + 1
                x4 = html[x1+1:].index(">") + x1 + 1
            except:
                break
            if x4<=x2:
                x2 = x4


            tag = html[x1+1:x2]
            trigger = False
            for x in self.avoidAttributes:
                if x in html[x1+1:x4]:
                    trigger = True
            if not tag in self.skipElements and "/" not in tag and not trigger:
                print(f"X1: {x1}  X2: {x2}")
                try:
                    pass#print(f"html: {html[x1-20:x2+ 30]}")
                except:
                    pass
                #print(f"Tag: {tag}")
                newPath = path + f'/{tag}'
                #print(f"newPath: {newPath}")
                i = 1
                #print(html[0:100])
                done2 = True
                #print("Before")
                while done2:
                    if i >= 100:
                            print("I is greater than 100")
                    if not (newPath + f'[{i}]') in self.paths:
                        self.paths.append(newPath + f'[{i}]')
                        done2 = False
                    else:
                        i+=1
                #print("After")
                html = html[x2:]
                if len(html) >= 3:
                    try:
                        x3 = html.index('<')
                    except:
                        x3 = 1
                    #print("/ not found " +html[x3+ 1])
                    if not html[x3 + 1] == "/" and not tag in self.noClosingElements:
                        #print("/ not found " +html[x3+ 1])
                        try:
                            total+=  1 + self.xPath(self.driver.find_element_by_xpath(newPath + f'[{i}]').get_attribute('innerHTML'), newPath + f'[{i}]', None)   
                        except:
                            print("Failed to get xpath from inner html.*******************************************************************************")    
                    else:
                        #print("/ found")
                        html = html[x3 + 1:] 
            else:
                html = html[x2:]
                if len(html) >= 3:
                    try:
                        x3 = html.index('<')
                    except:
                        x3 = 1
                    #print("/ not found " +html[x3+ 1])
                    if not html[x3 + 1] == "/" and not tag in self.noClosingElements:
                        pass
                    else:
                        #print("/ found")
                        html = html[x3 + 1:]
        return total
        #/html/body/div[1]/div/div[2]/div/ul/li[1]/ul/li[9]/a
        #/html/body/div[1]/div[1]/div[2]/div[1]/ul[1]/li[1]/ul[1]/li[10]/a


    '''def getXPaths(self, url, filename):
        if not self._setupScrap():
            logger.critical(f"driver setup failed")
        
        self.driver.get(url)
        #self.driver.mana   manage().timeouts().implicitlyWait(10)
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '*'))
            )
        except:
            print("webwait failed")

        #time.sleep(5)
        
        elements = self.driver.find_elements(By.TAG_NAME,'html')
        tags = []
        self.driver.implicitly_wait(0.00001)
        self.paths = []
        #self.index = 0
        self.paths.append('/html')
        for x in elements:
            #print(x.get_attribute("innerHTML"))
            subElems = x.find_elements_by_xpath(".//*")
            print(f'Final Total: {self.xPath(subElems,"/html")}')


        allpaths=""
        for x in self.paths:
            #print(x)
            #x = x.replace('[1]', '')
            #print(x)
            allpaths+= f"\n{x}"
            
        file = open(filename + ".txt",'w')
        file.write(allpaths)
        file.close()

        
        return self.paths


    def xPath(self, elems, path):
        index = 0
        childnum = 0
        while len(elems) >= index + 1:
            if index%30 == 0 and index !=0:
                print(f"Completed {index} of {len(elems)}" )
            if index == 100 and index !=0:
                return 1
            i = 1
            while True:
                    if not (path +'/' + elems[index].tag_name + f'[{i}]') in self.paths:
                        new = path + '/' + elems[index].tag_name + f'[{i}]'
                        
                        if elems[index].tag_name == 'svg':
                            clas = elems[index].get_attribute('class')
                            new = f'svg {clas}'   #f'//svg[@class="{clas}"][@viewbox="{viewbox}"]'
                            #print(str(at))
                            
                        if 'path' not in new: 
                            self.paths.append(new)
                        #print(path + '/' + elems[index].tag_name + f'[{i}]')
                        #print(path + '/' + elems[index].tag_name + f'[{i}]                      Index: {index}')
                        break
                    else:
                        i+=1
            try:
                subElems = elems[index].find_elements_by_xpath(".//*")
            except:
                subElems = []
            subSize = self.xPath(subElems, path + '/' + elems[index].tag_name + f'[{i}]')
            index += subSize + 1
            childnum+=1
        return index

    def login(self,url):
        if not self._setupScrap():
            logger.critical(f"driver setup failed")
    
        self.driver.get(url)
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "img"))
            )
        except:
            print("webwait failed")'''

    def infoGrabber2(self):
        
        time.sleep(20)
        print("done sleep")
        data = []


        self.ws = Xlsx('NGen.xlsx', "Sheet")
        for x in range(1):
            table = self.driver.find_element_by_xpath("/html/body/div/div[4]/div[1]/table/tbody")

            rows = table.find_elements_by_xpath(".//*")

        
            i = 0
            while True:

                html = rows[i].get_attribute("innerHTML")
                
                x1 = html.index('==">')
                x2 = html[x1:].index('</a>') + x1
                name = html[x1+4:x2]
                
                html = html[x2:]
                x3 = html.index('Eq">')
                x4 = html[x3:].index('</td>') + x3
                location = html[x3+4:x4]
                html = html[x4:]
                x5 = html.index('span>')
                x6 = html[x5:].index('</span') + x5
                orgtype = html[x5 + 5:x6]
                html = html[x6:]
                try:
                    x7 = html.index('href=')
                    x8 = html[x7:].index("rel") + x7
                    url = html[x7+6:x8-2]
                except:
                    url = "None"
                    i-=1
                    print([name, location, orgtype, url])
                company = [name, location, orgtype, url]
                #print(company)
                data.append(company)
                self.ws.addRows(company)
                i+= 8
                if i >= len(rows):
                    break
            print(x)
            if x!= 150:
                button = self.driver.find_element_by_xpath("/html/body/div/div[4]/div[2]/button[2]")
                button.click()
                time.sleep(0.05)
            else:
                print("else")

        self.ws.set_col_widths(40)
        self.ws.saveWorkbook()

        
            



    def xPath2(self, html, path, element):
        #print(f"Path: {path} Paths: {self.paths}")

        done = False
        total = 0
        while not done:
            #print("Html\n" + html[0:200])
            try:
                x1 = html.index('<')
            except:
                break
            try:
                x2 = html[x1+1:].index(" ") + x1 + 1
                x4 = html[x1+1:].index(">") + x1 + 1
            except:
                break
            if x4<=x2:
                x2 = x4


            tag = html[x1+1:x2]
            
            trigger = False
            for x in self.avoidAttributes:
                if x in html[x1+1:x4]:
                    trigger = True
            
            if not tag in self.skipElements and "/" not in tag and not trigger:
                print(f"X1: {x1}  X2: {x2}")
                try:
                    pass#print(f"html: {html[x1-20:x2+ 30]}")
                except:
                    pass
                print(f"Tag: {tag}")
                newPath = path + f'/{tag}'
                #print(f"newPath: {newPath}")
                i = 1
                #print(html[0:100])
                done2 = True
                subHTML = "************"
                #print("Before")
                while done2:
                    if i >= 100:
                            print("I is greater than 100")
                    if not (newPath + f'[{i}]') in self.paths:
                        self.paths.append(newPath + f'[{i}]')
                        done2 = False
                    else:
                        i+=1
                #print("After")
                print(html[0:x4 + 3])
                html = html[x4:]
                if len(html) >= 3:
                    try:
                        x3 = html.index('<')
                    except:
                        x3 = 1
                    #print("/ not found " +html[x3+ 1])
                    if not html[x3 + 1] == "/" and not tag in self.noClosingElements:
                        #print("/ not found " +html[x3+ 1])
                        try:
                            subHTML = self.driver.find_element_by_xpath(newPath + f'[{i}]').get_attribute('innerHTML')
                            total+=  1 + self.xPath2(subHTML, newPath + f'[{i}]', None)   
                        except:
                            print(f"Failed to get xpath from inner html. {newPath}*******************************************************************************")    
                    else:
                        #print("/ found")
                        pass #html = html[x3 + 1:]
                    try: 
                        x4 = html.index(subHTML)
                    except:
                        x4 = 0
                    x5 = len(subHTML)
                    html = html[x4 + x5:]

            '''else:
                html = html[x2:]
                if len(html) >= 3:
                    try:
                        x3 = html.index('<')
                    except:
                        x3 = 1
                    #print("/ not found " +html[x3+ 1])
                    if not html[x3 + 1] == "/" and not tag in self.noClosingElements:
                        pass
                    else:
                        #print("/ found")
                        #html = html[x3 + 1:]
                        pass'''
            

            depth = 0
            #print(f'start depth: {depth}')
            '''while True:
                
                x3 = html.index('<')
                try:
                    x2 = html[x3+1:].index(" ") + x3 + 1
                    x4 = html[x3+1:].index(">") + x3 + 1
                except:
                    print(html)
                    break
                if x4<=x2:
                    x2 = x4
                tag = html[x3+1:x2]
                print(f'depth tag: {tag}')
                print(f'Html: {html[x1-10:x2 + 10]}')
                if "/" in tag or tag in self.noClosingElements:
                    depth-=1
                else:
                    depth+=1
                
                print(f'depth: {depth}')
                if depth >=0 or depth >= 5:
                    print("Breaking")
                    break

                html = html[x3 + 2:]'''


        return total
        #/html/body/div[1]/div/div[2]/div/ul/li[1]/ul/li[9]/a
        #/html/body/div[1]/div[1]/div[2]/div[1]/ul[1]/li[1]/ul[1]/li[10]/a


        




#/html/body/div[1]/div/div[1]/a/img
    def nonText(self,url, data):
        altNum  = 10
        nameNum = 8
        idNum   = 9
        ariaNum = 11
        classNum = 7

        nonTextElems = ['img', 'button', 'input', 'video']
        
        elements = []
        #print(data)
        for item in data:
            
            #print(item)

            #if nonText
            if item[5] == "True":
                xPath = item[4]#.replace('[1]', '')
                #elem = self.driver.find_element_by_xpath(xPath)
                #elements.append(self.driver.find_element_by_xpath(xPath))
                elements.append({'type': item[2],'attributes': item, 'element': None, 'errors': [], 'xPath': xPath})
                #print(elements)
            #except:
                #print(f'Failed Path: {item}')
        
        #print(elements)
        for item in elements:
            #print(item)
            
            # Get name and alt text
            try:
                alt = item['attributes'][altNum]
                #print(f"alt: {alt}")
            except:
                item['errors'].append("WCAG 1.1.1 - All non-text content should have an alt text.")
                alt = "Broke"
            #print(f"alt: {alt}")
            try:
                name = item['attributes'][nameNum]
                #print(f"name: {name}")
            except:
                item['errors'].append("Non-text content should have a name. Controls Must have a name.")
                name = ""
            #item['errors'].append(f"Id: {item['attributes'][idNum]}")
            try:
                if item['type'] == "input" or item['type'] == "button":
                    aria = item['attributes'][ariaNum]
                    if not aria  == "":
                        alt = aria
                    else:
                        item['errors'].append("WCAG 1.1.1 - Control did not have an aria label to replace alt.")
                elif "captcha" in item['attributes'][classNum]:
                    item['errors'].append("WCAG 1.1.1 - Exception: Captcha not tested for alt text.")
            except:

                pass
        
            #Is displayed
            #Error not displayed - never displayed?
            
            #item['errors'].append(f"alt = {alt}")
            
            item['attributes'] = (f"Name: {name}   Alt: {alt}.  ")
            #print(item['attributes'])
            
            # Test for name and alt text
            if not len(str(alt)) >= 1:
                item['errors'].append("WCAG 1.1.1 - All non-text content should have an alt text.")

            if not len(str(name)) >= 1:
                item['errors'].append("Non-text content should have a name. Controls Must have a name.")

            # compare textdistance
            temp = None#textdistance.jaro_winkler(str(name).lower(), str(alt).lower())
            if temp <= .2:
                item['errors'].append(f"WCAG 1.1.1 - Name of element should match alt text or aria-label.")
        
        #print(elements)
        return elements

        '''self.ws = Xlsx('WWC.xlsx', "Sheet1")
        for x in elems:
            self.ws.addRows([x['type'], x['attributes'], x['errors']])
    
        self.ws.set_col_widths(80)
        self.ws.saveWorkbook()
        self.driver.close()'''
    def openElem(self, url, xpath):
        
        self.driver.get(url)
        self.driver.find_element_by_xpath(xpath)

    def openWebElement(self, url, xPath):
        #webid = 251
        print(xPath)
        #xPath = xPath.replace('[1]', '')
        print(xPath)
        item = self.driver.find_element(By.XPATH,xPath)
         
        y = item.location["y"]
        try:
            imgutils.scroll_to_Coordinate_Y(self.driver, y - 30)
        except:
            imgutils.scroll_to_Coordinate_Y(self.driver, y)
        imgutils.highlight_element(self.driver, item,"red", 3)

        print(item.getroottree().getpath(item))

        print("openElem done")
    

    def openSite(self, url):
        if not self._setupScrap():
            logger.critical(f"driver setup failed")
        
        self.driver.get(url)
        print("Success")
        #self.driver.find_element(By.CLASS_NAME,"ule-onboarding-continue-button").click()
        #self.driver.find_element(By.CLASS_NAME,"playButton").click()
        

    def getAllAttributes(self, url, xPath):
        self.driver.implicitly_wait(0.01)
        elem = 0
        ats = {'type': "", 'nonText': "False", 'decorative': "False" , 'class': "", 'name': '', 'id': "", 'alt': '', 'aria-label': '', 'src': '',
               'parent': '', 'children': '', 'role': "", 'aria-required': '', 'aria-describedby': '', 'tabindex': "", 'aria-current': '', 'aria-hidden': '', 
               'target': '', 'title': '', 'href': '', 'text': '', 'type id': '', 'scope': '', 'imgText': '', 'data-src': '', 'imgTable': '', 'imgIcon': '', 'srcset': '', 'lang': '', 'innerHTML': '', 'fontSize': ''}
        
        if 'svg' in xPath and not 'path' in xPath:
            if not "None" in xPath:
                try:
                    elem = self.driver.find_element_by_css_selector(f"svg[class='{xPath[4:]}'")
                except:
                    elem = False
        else:
                try:
                    elem = self.driver.find_element_by_xpath(xPath)
                except:
                    elem = False
        if elem:
            try:
                #xPath = xPath.replace('[1]', '')
                
                
                #ats = {'type': "", 'nonText': "False", 'decorative': "False" , 'class': "", 'name': '', 'id': "", 'alt': '', 'aria-label': '', 'src': ''}
                
                
                
                for at in ats:
                    try:
                        
                        ats[at] = elem.get_attribute(at)
                        
                        
                    except:
                        pass #no attribute
                ats['type'] = elem.tag_name
                try:
                    ats['text'] = elem.text
                except:
                    ats['text'] = ""
                try:
                    ats['fontSize'] = elem.value_of_css_property("font-size")
                except:
                    ats['fontSize'] = ''
                ats['nonText'] = 'False'
                ats['decorative'] = 'False'
                short = xPath[1:]
                x = -5
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
                ats['parent'] = xPath[0:len(xPath)-len(short)]
                
            except Exception as e:
                pass 
                #print(e)
            if elem != 0:
                attrs = self.driver.execute_script('var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;', elem)
                if ats['type'] == "audio":
                    #print(attrs)
                    pass
            
            try:
                #nontext
                if ats['type'] in ['img', 'form', 'button', 'input']:
                    ats['nonText'] = "True"
                #decorative
                if ats['type'] in ['img', 'source']:
                    #ats['imgText'] = 
                    ats = self.imageData(elem, ats)
            except Exception as e:
                print(f"Error in image converting {e}")

        
        return ats

    def imageData(self, elem, ats):
        #print(ats['type'])
        #https://stackoverflow.com/questions/59829470/pyinstaller-and-tesseract-ocr
        opener = urllib.request.URLopener()
        opener.addheader('User-Agent', "whatevers")
        filePath = r'.\\temp\\'
        #print("In imageData")
        try:
            
            src = ats['src']
            if ats['data-src'] != None:
                if len(ats['data-src']) > 2 and "hide-for-small" in ats['class']:
                    print("changing to data-src")
                    src = "https://www." + self.parseUrlBaseFromLink(self.url) + ats['data-src']
                    ats['data-src'] = src
                    print(src)
            if ".png" in src or '.jpg' in src:
                filename, headers = opener.retrieve(src, filePath + "img.png")
                #print("Found png")
            elif ".webp" in src:
                filename, headers = opener.retrieve(src, filePath + "oldImg.webp")
                dwebp(filePath + "oldImg.webp", filePath + "img.png", "-o")
                #print("Converted webp")
            elif ".jpg" in src:
                filename, headers = opener.retrieve(src, filePath + "oldImg.jpg")
                cwebp(filePath + "oldImg.jpg", filePath + "oldImg2.webp", "-o")
                dwebp(filePath + "oldImg2.webp", filePath + "img.png", "-o")
                #print("Converted jpeg")
            elif ".svg" in src:
                filename, headers = opener.retrieve(src, filePath + "oldImg.svg")
                im = svg2rlg(filePath + "oldImg.svg")
                renderPM.drawToFile(im, filePath + "img.png", fmt="PNG")
                print("Converted svg")
        except Exception as e:
            pass
            #print(f"Error in image converting {e}: ats: {ats}")
        #print('Before text detect:')
        #time.sleep(3)
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
        try:
            text = pytesseract.image_to_string(filePath + 'img.png')
        except:
            text = ""
        shutil.copyfile(filePath + "img.png", filePath + ats['alt'].replace(' ', "").replace('.', '').replace('\\', '') + "img.png")
        print(f'text: {text}')
        try:
            os.remove(filePath + "img.png")
        except:
            pass
        #check for table
        ats['imgText'] = text
        ats['imgTable'] = False
        ats['imgIcon'] = False
        return ats


    def loadXPaths(self, filename):
        f = open(filename + ".txt", "r")
        self.paths = []

        content = f.read()

        self.paths = content.split("\n")
        return self.paths

    def checkImgDec(self, elem, ats):
        #True if decorative
        if ats['type'] != "img":
            return False, "Not an image"
        width = elem.get_attribute('width')
        height = elem.get_attribute('height')

        #download image
        #convert image
        opener = urllib.request.URLopener()
        opener.addheader('User-Agent', "whatevers")
        try:
            filePath = r'.\\temp\\'
            src = ats['src']
            if ".png" in src:
                filename, headers = opener.retrieve(src, filePath + "img.png")
                #print("Found png")
            elif ".webp" in src:
                filename, headers = opener.retrieve(src, filePath + "oldImg.webp")
                dwebp(filePath + "oldImg.webp", filePath + "img.png", "-o")
                #print("Converted webp")
            elif ".jpg" in src:
                filename, headers = opener.retrieve(src, filePath + "oldImg.jpg")
                cwebp(filePath + "oldImg.jpg", filePath + "oldImg2.webp", "-o")
                dwebp(filePath + "oldImg2.webp", filePath + "img.png", "-o")
                #print("Converted jpeg")
            elif ".svg" in src:
                filename, headers = opener.retrieve(src, filePath + "oldImg.svg")
                im = svg2rlg(filePath + "oldImg.svg")
                renderPM.drawToFile(im, filePath + "img.png", fmt="PNG")
                #print("Converted svg")
        except Exception as e:
            pass
            #print(f"Error in image converting {e}")      

        
        #image to string
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
        #pytesseract.options(0.3, rgb='grayscale')
        #try:
        text = pytesseract.image_to_string(filePath + 'img2.png')
        #print(f"text: {len(text)} --- {text}")
        if len(text) >= 4:
            
            return False, "Text on image"
        #except:
         #   pass


        #other processes
        try:
            ratio = int(width)/int(height)
        except:
            ratio = 1
        if ratio >= 20 or ratio <= 0.1:
            return True, "Aspect Ratio too high"


        try:
            role = elem.get_attribute('role')
            if role == 'decorative':
                return True, "Role labeled as decorative."
            '''displayed = elem.is_displayed()
            if not displayed:
                return True, "Invisable"'''
        except:
            pass
        return True, "passed tests"
        #

    @classmethod
    def defaultDesktop(
        cls, url: str, navdepth: int, driver="Chrome", targetDevice=None
    ):
        return cls(url=url, navdepth=navdepth, driver=driver, targetDevice=targetDevice)

    @classmethod
    def defaultAndroid(cls):
        raise NotImplemented

    def sayHi(self):
        print("Hi")

    @classmethod
    def defaultiOS(cls):
        raise NotImplemented

    @staticmethod
    def parseUrlBaseFromLink(url: str) -> str:
        base = urlparse(url).netloc
        if 'www.' in base:
            first, *last = base.split('.')
            return '.'.join(last)
        else:
            return base

    @staticmethod
    def checkUrlValid(url: str) -> bool:
        try:
            response = requests.get(url)
        except Exception as exception:
            return False
        else:
            return True

    def getBaseUrl(self) -> str:
        return self.baseUrl

    def checkDomain(self, url: str) -> bool:
        return True if url == self.baseUrl else False

    def getNavDepth(self) -> int:
        return self.navdepth

    def checkUrlVisited(self, url: str) -> bool:
        return True if url in self.urlVisited else False

    def appendUrlVisited(self, url: str) -> None:
        self.urlVisited.add(url)

    def pushUrlQueue(self, link: Tuple[int, str]) -> None:
        self.urlQueue.appendleft(link)

    def popUrlQueue(self) -> Tuple[int, str]:
        return self.urlQueue.pop()

    def checkUrlQueue(self) -> int:
        return len(self.urlQueue)

    def convertToBinaryData(self,filename):
    #Convert digital data to binary format
        with open(filename, 'rb') as file:
            blobData = file.read()
        return blobData


    def findImages(self, url: str, driver: WebDriver) -> Tuple[List[ImageElementData], Optional[str]]:

        imgError = None
        data: List[ImageElementData] = list()
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "img"))
            )
            images = driver.find_elements(By.TAG_NAME, "img")
            for image in images:
                #print(image)
                #self.countImagesTotal+=1
                if self.screenshots:
                    imgutils.highlight_element(self.driver, image, "red", 3)
                    file_path = imgutils.scrollAndScreenshotElement(self.driver, image, self.img_count)
                    screenshot = self.convertToBinaryData(file_path)
                else:
                    screenshot = "NA"
                opener = urllib.request.URLopener()
                opener.addheader('User-Agent', "whatevers")
                try:
                    filePath = r'.\\temp\\'
                    src = image.get_attribute('src')
                    if ".png" in src:
                        filename, headers = opener.retrieve(src, filePath + "img.png")
                        print("Found png")
                    elif ".webp" in src:
                        filename, headers = opener.retrieve(src, filePath + "oldImg.webp")
                        dwebp(filePath + "oldImg.webp", filePath + "img.png", "-o")
                        print("Converted webp")
                    elif ".jpg" in src:
                        filename, headers = opener.retrieve(src, filePath + "oldImg.jpg")
                        cwebp(filePath + "oldImg.jpg", filePath + "oldImg2.webp", "-o")
                        dwebp(filePath + "oldImg2.webp", filePath + "img.png", "-o")
                        print("Converted jpeg")
                    elif ".svg" in src:
                        filename, headers = opener.retrieve(src, filePath + "oldImg.svg")
                        im = svg2rlg(filePath + "oldImg.svg")
                        renderPM.drawToFile(im, filePath + "img.png", fmt="PNG")
                        print("Converted svg")
                    else:
                        logger.error(f"Could not figure out image type. {src}")
                        logger.error(e, exc_info=True)
                        
                    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
                    print(pytesseract.image_to_string(filePath + "img.png"))
                        
                    #print(filePath)
                    
                    
                    img = self.convertToBinaryData(filePath + "img.png")
                    #self.countImagesDownloaded+=1
                   
                except Exception as e:
                    #print("no image gotten " + str(e))
                    img = "NA"
                #print(img)
                #img = self.convertToBinaryData("temp/img_ " + str(self.img_count) + ".png")
                '''signal = {'urlTotal': self.countUrlTotal, 'urlDomain':self.countUrlDomain, 'urlErrors': self.countUrlErrors,
                 'urlExternal': self.countUrlExternal, 'urlInvalid':self.countUrlInvalid, 'imgDownloaded': self.countImagesDownloaded,
                  'imgErrors': self.countImagesErrors, 'imgScrapped': self.countImagesScrapped, 'imgTotal': self.countImagesTotal, 'imgScreenshoted':self.countImagesScreenshot}
                print(signal)
                self.signalData2.emit(signal)'''
                #self.img_count = self.img_count + 1
                data.append(
                    ImageElementData(
                        url,
                        image.get_attribute("id"),
                        image.get_attribute("name"),
                        image.get_attribute("src"),
                        image.text,
                        image.get_attribute("alt"),
                        image.get_attribute("width"),
                        image.get_attribute("height"),
                        image.location["x"],
                        image.location["y"],
                        image.is_displayed(),
                        screenshot,
                        img
                    )
                )
                '''WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "image")))
                cssImg = self.driver.find_element_by_css_selector('image')
                for item in cssImg:
                    print(item)'''
        except Exception as e:
            logger.error(f"{e}")
            logger.error(e, exc_info=True)

            imgError = url
            data.clear()


        return (data, imgError)

    #def cssImages(self):
        
    def scrapButtons(self):
        raise NotImplementedError


    def findLinks(self, url:str, depth: int, driver: WebDriver) -> Tuple[List[linkElementData], Optional[str]]:

        linksError = None

        data: List[linkElementData] = list()
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "a"))
            )

            links = driver.find_elements(By.TAG_NAME, "a")

            for link in links:
                try:
                    temp: str = link.get_attribute("href")
                except Exception as e:
                    print(e)
                    temp: str = True
                if not temp:
                    logger.warning(f"found link with href \'None\' on parent page {url}")
                    continue
                self.pushUrlQueue((depth + 1, temp))
                data.append(
                    linkElementData(
                        temp,
                        None
                    )
                )
        except Exception as e:
            logger.error(f"{e}")
            logger.error(e, exc_info=True)

            linksError = url
            data.clear()

        return (data, linksError)

    
    def scrapUrl(
        self, url: str, depth: int = 1, option: List[str] = list()
    ) -> Tuple[
        List[linkElementData],
        Optional[str],
        List[ImageElementData],
        Optional[str],
        Optional[str]
        ]:

        linkData: List[linkElementData] = list()
        imageData: List[ImageElementData] = list()
        linkError:Optional[str] = None
        imageError:Optional[str] = None
        urlError:Optional[str] = None

        try:
            self.driver.get(url)    #type:ignore
        except Exception as e:
            logger.error(f"{e}")
            logger.error(e, exc_info=True)
            urlError = url
        else:
            linkData, linkError = self.findLinks(url, depth, self.driver)   #type:ignore
            imageData, imageError = self.findImages(url, self.driver)   #type:ignore
            #l, f = self.scarcssimage()
            self.appendUrlVisited(url)
        # finally:
        return (linkData, linkError, imageData, imageError, urlError)

    def scrapSite(self):

        duplicate:Optional[str] = None

        if not self._setupScrap():
            logger.critical(f"driver setup failed")

        try:
            while self.checkUrlQueue() > 0:

                url: str = ""
                depth: int = 0
                flagScrap = True

                linkData:List[linkElementData] = list()
                linkError:Optional[str] = None
                imageData:List[ImageElementData] = list()
                imageError:Optional[str] = None
                urlError:Optional[str] = None
                invalid:Optional[str] = None
                external:Optional[str] = None

                depth, url = self.popUrlQueue()
                logger.info(f"processing url {url}, depth: {depth}")

                if self.getNavDepth() != 0 and depth > self.getNavDepth():
                    logger.info(f"scrap skipping navdepth exceeded {depth} {url}")
                    continue
                
                if self.checkUrlVisited(url):
                    logger.info(f"scrap skipping url visited {depth} {url}")
                    duplicate = url
                    continue

                if not Scrap.checkUrlValid(url):
                    invalid = url
                    flagScrap = False

                if not self.checkDomain(Scrap.parseUrlBaseFromLink(url)):
                    external = url
                    flagScrap = False

                if flagScrap:
                    linkData,\
                    linkError,\
                    imageData,\
                    imageError,\
                    urlError = self.scrapUrl(url, depth)

                yield linkData,linkError,imageData,imageError,urlError,invalid,external,duplicate

        except Exception as e:
            warnings.warn(f"{e}")
            traceback.print_exc()
            return
