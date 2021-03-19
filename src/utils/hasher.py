# -*- coding: utf-8 -*-

from hashlib import md5
from typing import Tuple, Union, List, Set

U = Union[str, int, float, bool]
def createHashMD5(hlist: Union[List[U],Tuple[U], Set[U]]) -> str:

    h = md5()
    for h_ in hlist:
        if isinstance(h_, str):
            h.update(h_.encode('utf-8'))
        else:
            h.update(str(h_).encode('utf-8'))

    return h.hexdigest()