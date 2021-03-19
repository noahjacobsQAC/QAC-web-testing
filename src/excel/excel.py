# -*- coding: utf-8 -*-

import xlsxwriter


#logger = logging.getLogger(__name__)

# class Xlsx(Sheet):

#     book = Workbook()

#     def __init__(self, filename):
#         Sheet.__init__(self)

class Xlsx:

    

    def __init__(self, filename, sheetName):
        self.fileName = filename
        self.book = xlsxwriter.Workbook(filename)
        self.sheet = self.book.add_worksheet(sheetName)
        self.row = 0
        self.text_format = self.book.add_format({'text_wrap': True})
        i = 0
        columns=['image location', 'web screenshot', 'mobile screenshot', 'web image data',
                             'mobile image data']
       # for item in columns:
            #self.sheet.write(0,i,item)

 
    def addSheet(self, sheetname, columns):
        a = 2
        #self.book.create_sheet(sheetname).append(columns)

    def set_word_wrap(self, sheetname):
        for row in self.sheet.iter_rows():
            for cell in row:
                cell.alignment =  cell.alignment.copy(wrapText=True)

    def set_col_widths(self, width):
        '''self.sheet.column_dimensions["A"].width = 60
        self.sheet.column_dimensions["B"].width = 60
        self.sheet.column_dimensions["C"].width = 60
        self.sheet.column_dimensions["D"].width = 60
        self.sheet.column_dimensions["E"].width = 60'''
        self.sheet.set_column(0,5, width)
        '''for i in range(self.row):
            self.sheet.set_row(i + 1, 30)'''

    def getSheetNames(self)->list:

        return self.book.sheetnames


    # ? method not exposed currently
    def __getSheetByName(self, sheetname):

        return self.sheet


    def deleteSheet(self, sheetname):
        self.book.remove_sheet(self.sheet)

    def addToRow(self,col,item):
        self.sheet.write(self.row,col,str(item), self.text_format)
        self.row = self.row + 1

    def addRowsShifted(self, rows):
        for col_num, item in enumerate(rows):
            self.sheet.write(self.row + col_num,col_num, str(item),self.text_format)
        self.row = self.row + 1

    def addRows(self, rows):
        for col_num, item in enumerate(rows):
            self.sheet.write(self.row,col_num, str(item),self.text_format)
        self.row = self.row + 1

        '''active = self.sheet

        for row in rows:
            active.append(row)'''


    # todo add docstring or this method
    def editAtCell(self, sheetname, row, column, value):

        if sheetname not in self.book.sheetnames:
            print(f'sheet {sheetname} not present in workbook')
            return None

        '''active = self.sheet
        active.cell(column=column, row=row, value=f'{value}')'''


    # ? method not exposed. use generic addRows()
    def __addRow(self, sheetname, row):

        if sheetname not in self.book.sheetnames:
            print(f'sheet {sheetname} not present in workbook')
            return None



        '''active = self.sheet
        active.append(row)'''


    def editSheetName(self):
        raise NotImplementedError


    def saveWorkbook(self):
        print("saving")
        self.book.close()
        # remove empty default sheet
        '''try:
            self.book.remove_sheet(self.book.get_sheet_by_name("Sheet"))
        except Exception as e:
            logger.warn(f'{e}')'''

        #self.book.save(self.fileName)





