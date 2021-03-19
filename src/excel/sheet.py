# -*- coding: utf-8 -*-

import abc

# ! pending
# TODO work on this soon, concrete class for worksheet

class Sheet:

    def __init__(self):
        pass

    def addRow(self, row):
        raise NotImplementedError


    def addRows(self, rows):
        raise NotImplementedError


    def addColumn(self):
        raise NotImplementedError


    def insertAtCell(self, value):
        raise NotImplementedError