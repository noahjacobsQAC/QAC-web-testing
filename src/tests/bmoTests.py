



from typing import Any, Deque, Dict, Iterable, List, Optional, Set, Tuple, Union

#import inspect

from PyQt5.QtCore import QThread, pyqtSignal


from src.database.wacdatabase import WACDatabase
import logging
import inspect
from src.logger import logger
from datetime import datetime
logger = logging.getLogger(__name__)
#from textdistance import jaro_winkler
from langdetect import detect
from fuzzywuzzy import fuzz


class BMOTests(QThread):
    signalConsole = pyqtSignal(str)
    signalFinished = pyqtSignal(bool)
    def __init__(
        self,
        url: str,
        
        scanID: str,
        
        
    ) -> None:

        super().__init__()
        self.scanID = scanID
        self.url = url
        self.numtype = 2
        self.numxpath = 4
        self.numalt = 5
        self.numariacurrent = 6
        self.numariadescribedby = 7
        self.numariahidden = 8
        self.numarialabel = 9
        self.numariarequired = 10
        self.numclass = 11
        self.numid = 12
        self.numname = 13
        self.numrole = 14
        self.numsrc = 15
        self.numtabindex = 16
        self.numtarget = 17
        self.numtitle = 18
        self.numhref = 19
        self.numtext = 20
        self.numscope = 21
        self.numimgtext = 22
        self.numlang = 27
        self.numfontsize = 29
       
        self.subSystemDatabase = WACDatabase("sqlite/database.db")
        
        

    
    def _setupScrap(self) -> bool:

        self.setupDriver()

        if not self.isDriverInitialized():
            print("driver not initialized!")
            return False

        
        return True

    #def run

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


    
       

    def run(self):
        data = self.subSystemDatabase.getSiteData('elements', self.scanID)
        print(f"Size of scan: {len(data)}")
        self.linkTest()
        self.formTest()
        self.headingTests()
        self.tableTest()
        self.videoframeTests()
        self.semanticTests()
        self.signalFinished.emit(True)


    def focusTests(self):
        # Rule 50
        ps = self.subSystemDatabase.getSiteTypeData("elements", self.scanID, "p")
        brs = self.subSystemDatabase.getSiteTypeData("elements", self.scanID, "br")
        for item in brs + ps:
            if item[self.numtext] == "" or item[self.numtext] == None:
                self.subSystemDatabase.addNotesToSite("elements", "Rule 50", item[self.numxpath], "CSS is used to adjust element’s position, rather than br elements or empty p elements.", self.scanID)
            
        
    
    def formTest(self):
        self.signalConsole.emit(f"Starting Form Tests.")
        data = self.subSystemDatabase.getSiteData('elements', self.scanID)
        inputs = self.subSystemDatabase.getSiteTypeData("elements", self.scanID, "input")
        buttons = self.subSystemDatabase.getSiteTypeData("elements", self.scanID, "button")
        fieldsets = self.subSystemDatabase.getSiteTypeData("elements", self.scanID, "fieldset")
        for item in inputs:
            parent = item[self.numxpath][0:len(item[self.numxpath]) - len(item[self.numtype])]
            # Rule 22
            check = False
            for x in data:
                if (x[self.numxpath][0:len(x[self.numxpath]) - len(x[self.numtype])]) == parent:
                    if x[self.numtype] == 'label':
                        check = True
            if not check:
                self.subSystemDatabase.addNotesToSite("elements", "Rule 22", item[self.numxpath], "Every input field has a descriptive label element associated with it.", self.scanID)
            
            # Rule 23
            #if required
            if not item[self.numariarequired] == "true":
                self.subSystemDatabase.addNotesToSite("elements", "Rule 23", item[self.numxpath], "Every input field that is required has an aria-required=true attribute.", self.scanID)

            # Rule 24
            if "fieldset" not in item[self.numxpath]:
                self.subSystemDatabase.addNotesToSite("elements", "Rule 24", item[self.numxpath], "Form fields that are grouped are contained within a fieldset element", self.scanID)

        for item in fieldsets:
        
            # Rule 25
            legend = self.subSystemDatabase.getElemByXPath('elements', self.scanID, item[self.numxpath] + "/legend[1]")
            if legend == False:
                self.subSystemDatabase.addNotesToSite("elements", "Rule 25", item[self.numxpath], "Every fieldset element has a descriptive legend element as it's first element.", self.scanID)
            #Should check if its the first element, would require attaching child order data


        # Rule 26
        # Unsure how to address
        self.signalConsole.emit(f"Form Tests complete.")

    def headingTests(self):
        self.signalConsole.emit(f"Starting Heading Tests.")


        # Rule 19
        # - how to identify/trigger modals
        modals = self.subSystemDatabase.getElemByClassContains('elements', self.scanID, "modal")
        for item in modals:
            ind = item[0]
            if self.subSystemDatabase.getElemByElemID('elements', self.scanID, ind + 1)[self.numtype] != 'h2':
                self.subSystemDatabase.addNotesToSite("elements", "Rule 19", item[self.numxpath], "Every modal has a descriptive h2 element as its first element.", self.scanID)
            
        # Rule 20
        # What is a tab? just the tab cycle?

        # Rule 27
        h1s = self.subSystemDatabase.getSiteTypeData("elements", self.scanID, "h1")
        if len(h1s) != 1:
            for item in h1s:
                self.subSystemDatabase.addNotesToSite("elements", "Rule 27", item[self.numxpath], "Every page has exactly 1 h1 element.", self.scanID)
            
        # Rule 28
        headings = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7']
        data = self.subSystemDatabase.getSiteData('elements', self.scanID)
        last = None
        for item in data:
            if item[self.numtype] in headings:
                if last == None:
                    last = item[self.numtype][1]
                else:
                    if (int(item[self.numtype][1]) - int(last)) > 1:
                        self.subSystemDatabase.addNotesToSite("elements", "Rule 28", item[self.numxpath], "Heading structure is respected, so that any sub-headings increment heading level by one.  Heading skip detected", self.scanID)

        # Rule 47
        # Grab sticky nav items
        for item in []:
            if item[self.numtabindex] != -1:
                self.subSystemDatabase.addNotesToSite("elements", "Rule 47", item[self.numxpath], "For sticky navs, section heading has a tabindex=-1 ", self.scanID)

        self.signalConsole.emit(f"Done Heading Tests.")



    def semanticTests(self):
        self.signalConsole.emit(f"Starting HTML Semantics Tests.")
        data = self.subSystemDatabase.getSiteData('elements', self.scanID)
        navs = self.subSystemDatabase.getSiteTypeData("elements", self.scanID, "nav")

        # Rule 21
        ids = []
        for item in data:
            print(item[self.numtype])
            if not item[self.numid] in ids or item[self.numid] == "":
                ids.append(item[self.numid])
            else:
                self.subSystemDatabase.addNotesToSite("elements", "Rule 21", item[self.numxpath], "No two elements share an ID on any given page.  Found same ID twice.", self.scanID)
                
        # Rule 41
        # - check for repetitivness that should be in lists?
        

        # Rule 42
        # - "All navigations" checking links or context?
        navigations = self.subSystemDatabase.getElemByClassContains('elements', self.scanID, 'nav')
        for item in navigations:
            if not 'nav' in item[self.numxpath]:
                self.subSystemDatabase.addNotesToSite("elements", "Rule 42", item[self.numxpath], "All navigations should be implemented using the nav element", self.scanID)

        for item in navs:
            arialabel = item[self.numarialabel]
            # Rule 43
            if arialabel == "" or arialabel == None:
                    self.subSystemDatabase.addNotesToSite("elements", "Rule 43", item[self.numxpath], "nav element should have an aria-label attribute.", self.scanID)


        for item in data:
            # Rule 44
            if 'nav' in item[self.numxpath]:
                if item[self.numhref] == self.url:
                    navPath = item[self.numxpath][0:item[self.numxpath].index('nav') + 6]
                    print(f'navpath: {navPath}')
                    self.subSystemDatabase.getElemByXPath('elements', self.scanID, navPath)
                    if not item[self.numariacurrent] == "page":
                        self.subSystemDatabase.addNotesToSite("elements", "Rule 44", item[self.numxpath], "Nav elements should have an aria-label attribute. None found.", self.scanID)
            
        # Rule 45
        mains = self.subSystemDatabase.getSiteTypeData('elements', self.scanID, 'main')
        for item in mains:
            xpath = item[self.numxpath]
            children = self.subSystemDatabase.getElemByXPathContains('elements', self.scanID, xpath + '/')
            if children[0][self.numtype] != 'span':
                self.subSystemDatabase.addNotesToSite("elements", "Rule 45", item[self.numxpath], "A span with accessibility content and id='skip-nav' is the first element within main. Span was not found to be the first element.", self.scanID)
            elif children[0][self.numid] != 'skip-nav':
                self.subSystemDatabase.addNotesToSite("elements", "Rule 45", item[self.numxpath], "A span with accessibility content and id='skip-nav' is the first element within main. Span did not have id='skip-nav'.", self.scanID)


        # Rule 48
        trigger = True
        for item in data:
            if item[self.numtype] == 'section' or item[self.numtype] == 'article':
                trigger = False
                elem = item

        if trigger:
            self.subSystemDatabase.addNotesToSite("elements", "Rule 48", '/html', " HTML is structured using semantic layout ", self.scanID)

        # Rule 55
        html = self.subSystemDatabase.getElemByXPath('elements', self.scanID, '/html')
        print(html)
        if len(html[0][self.numlang]) < 2:
            self.subSystemDatabase.addNotesToSite("elements", "Rule 55", item[self.numxpath], "Language is explicitly defined within the page.", self.scanID)
        lang = html[0][self.numlang]
        # Rule 56
        for item in data:
            aria = item[self.numarialabel]
            alt = item[self.numalt]
            if aria == None:
                aria = ""
            if alt == None:
                alt = ''
            if len(aria) > 4:
                try:
                    arialang = detect(alt)
                except:
                    arialang = 'na'
                if arialang != lang:
                    self.subSystemDatabase.addNotesToSite("elements", "Rule 56", item[self.numxpath], "Accessibility Language matches that of the page.", self.scanID)
            if len(alt) > 4:
                try:
                    altlang = detect(alt)
                except:
                    altlang = 'na'
                if altlang != lang:
                    self.subSystemDatabase.addNotesToSite("elements", "Rule 56", item[self.numxpath], "Accessibility Language matches that of the page.", self.scanID)
        # Rule 57
        banner = self.subSystemDatabase.getElemByClass('elements', self.scanID, "primary-header__wrapper blue-bar-height-fix")
        if banner[0][self.numrole] != "alert":
            self.subSystemDatabase.addNotesToSite("elements", "Rule 57", item[self.numxpath], "Top blue banner has role=alert.", self.scanID)





        self.signalConsole.emit(f"HTML Semantics Tests completed. ")



    def imageTests(self):
        images = self.subSystemDatabase.getSiteTypeData("elements", self.scanID, "img")
        svgs = self.subSystemDatabase.getSiteTypeData("elements", self.scanID, "svg")
        pictures = self.subSystemDatabase.getSiteTypeData("elements", self.scanID, "picture")
        icons = self.subSystemDatabase.getElemByClassContains('elements', self.scanID, "icon")
        # Rule 12
        



        
        
        if len(images) < 1:
            self.subSystemDatabase.addNotesToSite("elements", "Rule 32", '/html/body[1]', "For SEO purposes, any given page has at least one image with alt text, even if it is for a decorative one. 0 images were detected.", self.scanID)
        check = True
        
        for item in images:
            text = item[self.numimgtext]
            alt = item[self.numalt]
            # Rule 30
            if text != None:
                if len(text) >= 2:
                    if len(alt) <= (0.5*len(text)):
                        self.subSystemDatabase.addNotesToSite("elements", "Rule 30", item[self.numxpath], "If image is informative, it has an informative alt attribute.", self.scanID)
    
            # Rule 31
            if text == None or len(text) <= 2:
                if alt != "":
                    self.subSystemDatabase.addNotesToSite("elements", "Rule 31", item[self.numxpath], "If image is decorative, it has an alt="" attribute.", self.scanID)
    

            
            # Rule 32
            if 'svg' in item[self.numsrc]:
                svgs.append(item)
            arialabel = item[self.numarialabel]
            if arialabel != "" and arialabel != None:
                check = False
            if check:
                self.subSystemDatabase.addNotesToSite("elements", "Rule 32", '/html/body[1]', "For SEO purposes, any given page has at least one image with alt text, even if it is for a decorative one. No alt text found on any images.", self.scanID)
            
            # Rule 33
            text = item[self.numtext]
            if text != "":
                score = fuzz.ratio(str(text).lower(), str(item[self.numalt]).lower())
                if score < 0.9:
                    self.subSystemDatabase.addNotesToSite("elements", "Rule 33", item[self.numxpath], "If image contains text, it has the exact same text as its alt attribute.", self.scanID)
            
            # Rule 35
            if 'icon' in item[self.numclass] and 'svg' not in item[self.numsrc]:
                self.subSystemDatabase.addNotesToSite("elements", "Rule 35", item[self.numxpath], "For every icon, being either a standalone svg element or a .svg file placed in an img element is the best practice", self.scanID)
            

        # Rule 34
        for item in svgs:
            alt = item[self.numalt]
            if item[self.numtitle] != "":
                self.subSystemDatabase.addNotesToSite("elements", "Rule 34", item[self.numxpath], "For every icon, does not have a title attribute nor a nested title tag.", self.scanID)
            #if has <title> in html

            #Rule 37
            if item[self.numtype] == 'img':
                if item[self.numalt] != "":
                    self.subSystemDatabase.addNotesToSite("elements", "Rule 37", item[self.numxpath], "If icon is a file in an img element it has an alt='' attribute.", self.scanID)
    
            # Rule 40
            #if chart
            if alt == '':
                if item[self.numariahidden] != "true":
                    self.subSystemDatabase.addNotesToSite("elements", "Rule 37", item[self.numxpath], "Every chart image itself has either a general alt attribute or alt='' aria-hidden=true attributes", self.scanID)
    
    

        for item in icons:
            text = item[self.numimgtext]
            if text != None and len(text) >=3:
                parentPath = item[self.numxpath][0:len(item[self.numxpath]) - len(item[self.numtype])]
                parent = self.subSystemDatabase.getElemByXPath('elements', self.scanID, parentPath)
                if 'show-for-sr' in parent[self.numclass]:
                    self.subSystemDatabase.addNotesToSite("elements", "Rule 38", item[self.numxpath], "For icons, adding tooltip content is the best practice but is not mandatory", self.scanID)
    
            title = item[self.numtitle]
            if title == None or title == "":
                self.subSystemDatabase.addNotesToSite("elements", "Rule 36", item[self.numxpath], "If icon is informative, a descriptive element with class show-for-sr is added either before or after every entry.", self.scanID)
    




    def linkTest(self):
        anchors = self.subSystemDatabase.getSiteTypeData("elements", self.scanID, "a")
        buttons = self.subSystemDatabase.getSiteTypeData("elements", self.scanID, "button")
        total = len(anchors) + len(buttons)
        seg = int(total/5)
        completed = 0
        errorcount = 0
        self.signalConsole.emit(f"Starting Link Tests on {total} elements.")
        for item in (anchors + buttons):
            print(f'{completed/total}   seg: {seg}')
            if completed%seg ==0:
                self.signalConsole.emit(str("%.2f" % (completed/total)) + "%")
            if item[2] == "button":
                print(item)
            arialabel: str = item[self.numarialabel]
            
            href = item[self.numhref]
            if href == None:
                href = ""
            text = item[self.numtext]
            # Rule 1 applied to all
            '''if arialabel == "" or arialabel == None:
                self.subSystemDatabase.addNotesToSite("elements", "Rule 1", item[self.numxpath], "Aria-Label is blank or missing.", self.scanID)'''
            # Rule 2
            #"Ambiguous or not unique" Compare all inputs, check if they have alt text
            for item2 in (anchors + buttons):
                if item[self.numtext] == item2[self.numtext]: #and item[self.numtext] != "":
                    if item[self.numarialabel] == "":
                        errorcount+=1
                        self.subSystemDatabase.addNotesToSite("elements", "Rule 2", item[self.numxpath], "For every anchor or button, if content is not unique, accessible content is provided.", self.scanID)
                
            # Rule 3
            if item[self.numtarget] == "_blank":
                if arialabel == "" or arialabel == None:
                    errorcount+=1
                    self.subSystemDatabase.addNotesToSite("elements", "Rule 3", item[self.numxpath], "Links/Buttons with target=_blank should provide templated accessible text that a new page will open. No aria-label found.", self.scanID)
                elif not "new page" in arialabel.lower():
                    errorcount+=1
                    self.subSystemDatabase.addNotesToSite("elements", "Rule 3", item[self.numxpath], "Links/Buttons with target=_blank should provide templated accessible text that a new page will open. 'new page' not found in aria-label.", self.scanID)
            # Rule 4
            if ".pdf" in href:
                if not "pdf" in arialabel.lower():
                    errorcount+=1
                    self.subSystemDatabase.addNotesToSite("elements", "Rule 4", item[self.numxpath], "Links/Buttons which link to a PDF, it provides templated accessible text that the element links to a PDF. 'pdf' not found in aria-label.", self.scanID)
            # Rule 5
            if "tel:" in href:
                if not "phone" in arialabel.lower():
                    errorcount+=1
                    self.subSystemDatabase.addNotesToSite("elements", "Rule 5", item[self.numxpath], "Links/Buttons which link to a phone number, it provides templated accessible text that the link opens a phone number. 'phone number' not found in aria-label.", self.scanID)

            # Rule 6
            if text == text.upper() and text != text.lower():
                errorcount+=1
                self.subSystemDatabase.addNotesToSite("elements", "Rule 6", item[self.numxpath], "For every anchor or button, the text for the element cannot be all capitals.", self.scanID)

            # Rule 7
            if text.lower() == href.lower() and text != "" and href != None:
                if arialabel == "" or arialabel == None:
                    errorcount+=1
                    self.subSystemDatabase.addNotesToSite("elements", "Rule 7", item[self.numxpath], "If the content matches the href, then an aria-label should be added.", self.scanID)
            
            # Rule 46
            #How to check for sticky navs
            if '#' in href:
                id = href[href.index('#') + 1:]
                if id != "":
                    types = self.subSystemDatabase.getTypeWhereColEquals('id', id, self.scanID)
                    for ob in types:
                        if ob[0] != "h1" or ob[0] != 'h2' or ob[0] != 'h3' or ob[0] != 'h4' or ob[0] != 'h5':
                            errorcount+=1
                            self.subSystemDatabase.addNotesToSite("elements", "Rule 46", item[self.numxpath], "For sticky navs, the link references the id of a section heading rather than the section itself. Detected that the element referenced a non header.", self.scanID)
                



            self.subSystemDatabase.conn.commit()
            completed+=1
        self.signalConsole.emit(f"Link Tests completed. Found {errorcount} errors.")


    def readerTests(self):
        hrs = self.subSystemDatabase.getSiteTypeData("elements", self.scanID, "hr")
        brs = self.subSystemDatabase.getSiteTypeData("elements", self.scanID, "br")

        # Rule 59
        for item in hrs + brs:
            if item[self.numariahidden].lower() != 'true':
                self.subSystemDatabase.addNotesToSite("elements", "Rule 59", item[self.numxpath], "Horizontal separator and line break has aria-hidden=true", self.scanID)
                








    def tableTest(self):
        self.signalConsole.emit(f"Starting Table Tests.")
        tables = self.subSystemDatabase.getSiteTypeData("elements", self.scanID, "tables")
        for item in tables:

            # Rule 8
            caption = self.subSystemDatabase.getElemByXPath('elements', self.scanID, item[self.numxpath] + "/caption[1]" )
            if len(caption) < 1:
                self.subSystemDatabase.addNotesToSite("elements", "Rule 8", item[self.numxpath], "Every table has a descriptive caption element (either visible or screen reader specific). No captions element found.", self.scanID)
    

            # Rule 9
            thead = self.subSystemDatabase.getElemByXPath('elements', self.scanID, item[self.numxpath] + "/thead[1]" )
            if len(thead) < 1:
                self.subSystemDatabase.addNotesToSite("elements", "Rule 9", item[self.numxpath], "Every table has an appropriate thead and tbody element. No thead found.", self.scanID)

            tbody = self.subSystemDatabase.getElemByXPath('elements', self.scanID, item[self.numxpath] + "/tbody[1]" )
            if len(tbody) < 1:
                self.subSystemDatabase.addNotesToSite("elements", "Rule 9", item[self.numxpath], "Every table has an appropriate thead and tbody element. No tbody found.", self.scanID)

            # Rule 10
            ths = self.subSystemDatabase.getSiteTypeData("elements", self.scanID, "th")
            check = True
            for th in ths:
                if item[self.numxpath] in th[self.numxpath]:
                    check = False
            if check:
                self.subSystemDatabase.addNotesToSite("elements", "Rule 10", item[self.numxpath], "Every table has appropriate th elements for the table header. No th found.", self.scanID)

            # Rule 11
            #Checking the table elem or the tr elems? td too?
            #if item[self.numscope] 
        self.signalConsole.emit(f"Table Tests complete.")

    def videoframeTests(self):
        self.signalConsole.emit(f"Starting iFrame/Video Tests.")
        frames = self.subSystemDatabase.getSiteTypeData("elements", self.scanID, "iframe")
        videos = self.subSystemDatabase.getSiteTypeData("elements", self.scanID, "video")
        buttons = self.subSystemDatabase.getSiteTypeData("elements", self.scanID, "button")

        # Rule 13
        for item in frames + videos:
            if item[self.numtitle] == None or item[self.numtitle] == "":
                self.subSystemDatabase.addNotesToSite("elements", "Rule 13", item[self.numxpath], "Every video or iframe has a descriptive title attribute. No title found.", self.scanID)
        self.signalConsole.emit(f"iFrame/Video Tests complete.")


        # Rule 14
        for item in videos:
            parentPath = item[self.numxpath][0:len(item[self.numxpath]) - len(item[self.numtype])]
            isYoutTube = False
            isIDPlayer = False

            for i in range(4):
                parent = self.subSystemDatabase.getElemByXPath('elements', self.scanID, parentPath)
                
                if parent[self.numarialabel] == "Youtube Video Player":
                    isYoutTube = True
                if parent[self.numid] == "player":
                    isIDPlayer = True
                parentPath = parent[self.numxpath][0:len(parent[self.numxpath]) - len(parent[self.numtype])]

            if not isYoutTube or not isIDPlayer:
                self.subSystemDatabase.addNotesToSite("elements", "Rule 14", item[self.numxpath], "Every video player has proper controllers.", self.scanID)
        
        trigger = True
        # Rule 15
        for item in buttons:
            if item[self.numclass] == 'ytp-subtitles-button ytp-button':
                trigger = False
            if trigger:
                self.subSystemDatabase.addNotesToSite("elements", "Rule 15", item[self.numxpath], " Every video player has BMO-generated captions", self.scanID)
        

      

        

    def visabilityTests(self):
        data = self.subSystemDatabase.getSiteData('elements', self.scanID)

        # Rule 51
        # Might want to switch to specific elements
        for item in data:
            font = self.numFontSize
            ind = font.index('p')
            size = int(font[0:ind-1])
            if size < 13:
                self.subSystemDatabase.addNotesToSite("elements", "Rule 51", item[self.numxpath], "Font size is at least 14px for any text in the page.", self.scanID)
        
