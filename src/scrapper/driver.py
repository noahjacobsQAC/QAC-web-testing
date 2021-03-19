# -*- coding: utf-8 -*-
# https://www.browserstack.com/docs/automate/selenium/getting-started/python
# https://gist.github.com/devinmancuso/ec8ae08fa73402e45bf1
# https://chromedriver.chromium.org/mobile-emulation
# https://www.guru99.com/chrome-options-desiredcapabilities.html

import platform
import inspect
import warnings
from typing import Dict, Optional, Union, Set

from selenium import webdriver  # type:ignore
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import (
    DesiredCapabilities,
)  # type:ignore

import logging
from src.logger import logger
logger = logging.getLogger(__name__)

class Driver:

    pathDriverL64gecko = r"./webdrivers/linux64/geckodriver"
    pathDriverD64gecko = r"./webdrivers/mac64/geckodriver"
    pathDriverW64gecko = r"./webdrivers/windows64/geckodriver.exe"
    pathDriverW64gecko = r"./webdrivers/windows/geckodriver.exe"
    pathDriverL64chrome = r"./webdrivers/linux64/chromedriver"
    pathDriverD64chrome = r"./webdrivers/mac64/chromedriver"
    pathDriverW64chrome = r"./webdrivers/windows/chromedriver.exe"

    supportedPlatforms: Set[str] = {"Linux", "Darwin", "Windows"}
    supportedDriver: Set[str] = {"Chrome", "Firefox"}

    mapPlatformDriver: Dict[str, Dict[str, str]] = {
        "Linux": {"Chrome": pathDriverL64chrome, "Firefox": pathDriverL64gecko},
        "Windows": {"Chrome": pathDriverW64chrome, "Firefox": pathDriverW64gecko},
        "Darwin": {"Chrome": pathDriverD64chrome, "Firefox": pathDriverD64gecko},
    }

    def __init__(
        self,
        webDriver: str,
        targetDevice: Optional[str] = None,
        timeout: int = 30,
        configuration: Optional[Dict] = None,
    ) -> None:

        self.webDriver: str = webDriver
        self.targetDevice: Union[str, None] = targetDevice
        self.pageLoadTimeOut: int = timeout
        try:
            self.headless: Optional[Dict] = configuration['headless']
        except:
            self.headless = False
        print("headless: " + str(self.headless))

        self.driver: Union[webdriver.Chrome, webdriver.Firefox, None] = None
        self.hostPlatform: str = ""
        self.emulatedDevice: Union[Dict, None] = None


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

    def getPlatform(self) -> Union[str, None]:

        return self.hostPlatform

    def getTargetDevice(self) -> Union[str, None]:

        return self.targetDevice

    def getEmulatedDeviceConfig(self) -> Union[Dict, None]:

        return self.emulatedDevice

    def isDriverInitialized(self) -> bool:

        return True if self.driver else False

    def setupDriver(self):

        self.hostPlatform = platform.system()

        if self.targetDevice:
            self.emulatedDevice = {"deviceName": self.targetDevice}

        if not self._driverSetup():
            warnings.warn(f"driver not initialized")

        self.driver.set_page_load_timeout(self.pageLoadTimeOut)
        self.driver.implicitly_wait(15)
        self.driver.set_script_timeout(15)

    @staticmethod
    def _getDriverPath(platform: str, driverString_: str) -> Optional[str]:

        return Driver.mapPlatformDriver.get(platform, None).get(driverString_, None)

    def _driverSetup(self) -> bool:

        driverPath: Optional[str] = None

        if self.webDriver not in Driver.supportedDriver:
            warnings.warn(f"{self.webDriver} driver not supported")
            return False

        if self.hostPlatform in Driver.supportedPlatforms:
            driverPath = Driver._getDriverPath(str(self.hostPlatform), self.webDriver)
        else:
            warnings.warn(f"platform not supported {self.hostPlatform}")
            return False

        if not driverPath:
            warnings.warn(f'driverPath entry not found "Driver.mapPlatformDriver"')
            return False

        if self.webDriver == "Chrome":
            self.driver = self._getDriverChrome(driverPath)
        elif self.webDriver == "FireFox":
            self.driver = self._getDriverFirefox(driverPath)

        if not self.driver:
            warnings.warn(f"driver not initialized")
            return False

        return True

    def _getDriverFirefox(self, executable_path) -> Union[webdriver.Firefox, None]:

        capabilities_ = DesiredCapabilities().FIREFOX.copy()
        capabilities_["marionette"] = False

        try:
            return webdriver.Firefox(
                capabilities=capabilities_,
                executable_path=executable_path,
                log_path=r"logs/gecko_driver.log",
            )
        except Exception as e:
            warnings.warn(f"{e}")
            return None

    def _getDriverChrome(self, executable_path) -> Union[webdriver.Chrome, None]:

        chrome_options_ = webdriver.ChromeOptions()
        if self.headless:
            chrome_options_.add_argument("--headless")
            chrome_options_.add_argument("--user-agent=foo")
        if self.emulatedDevice:
            chrome_options_ = webdriver.ChromeOptions()
            chrome_options_.add_experimental_option(
                "mobileEmulation", self.emulatedDevice
            )

        try:
            return webdriver.Chrome(
                executable_path=executable_path, chrome_options=chrome_options_
            )
        except Exception as e:
            warnings.warn(f"{e}")
            return None
