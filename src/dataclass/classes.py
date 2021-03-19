# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Any, Optional, Union
from collections import namedtuple

@dataclass
class ImageElementData:
    url: str = ""
    id: Union[Any] = None
    name: str = ""
    src: str = ""
    text: str = ""
    altText: str = ""
    width: Union[str, int, None] = None
    height: Union[str, int, None] = None
    x: Union[str, int, None] = None
    y: Union[str, int, None] = None
    displayed: bool = False
    download:  Union[Any] = None
    image: Union[Any] = None

@dataclass
class linkElementData:
    url: str = ""
    screenShot: Union[Any] = None

@dataclass
class ButtonElementData:
    pass

@dataclass
class BasicElementData:
    pass

nt_Entry = namedtuple(
    "nt_Entry",
    [
        'EMID',
        'url',
        'status',
        'description'
    ]
)

nt_ScrapSetting = namedtuple(
    "nt_ScrapSetting",
    [
        'SSID',
        'EMID',
        'HASHKEY',
        'driver',
        'targetPlatform',
        'navDepth',
        'date'
    ]
)

nt_ElementTableRef = namedtuple(
    "nt_ElementTableRef",
    [
        'ETRID',
        'SSID',
        'UrlTable',
        'ImgTable',
        'BtnTable'
    ]
)

prefix_EleUrlTable = "URL_"
prefix_EleBtnTable = "BTN_"
prefix_EleImgTable = "IMG_"
