import gspread
import time
from oauth2client.service_account import  ServiceAccountCredentials

class Dawet(object):
    def __init__(self, filename):
        self.filename = filename
        self.opendb()

    def opendb(self):
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('client_secrets.json', scope)
        client = gspread.authorize(creds)
        self.sheet = client.open(self.filename)

    def getAllData(self, sheetnum):
        list_value = self.sheet.get_worksheet(sheetnum).get_all_values()

        return list_value

    def getData(self, rowname, colname, sheetnum):
        dataError = True
        while dataError:
            try:
                ambil = self.sheet.get_worksheet(sheetnum).cell(self.sheet.get_worksheet(sheetnum).find(rowname).row, self.sheet.get_worksheet(sheetnum).find(colname).col).value
                print(colname + " selesai")
                dataError = False
                return ambil
            except Exception as e:
                print(e)
                if str(e) == rowname:
                    dataError = False
                    return "not_found"
                elif str(e) == colname:
                    dataError = False
                    return "pertemuan_not_found"
                else:
                    print("wait ...")
                    time.sleep(10)
                    dataError = True

    def setData(self, rowname, colname, sheetnum, content):
        setv = self.sheet.get_worksheet(sheetnum).update_cell(self.sheet.get_worksheet(sheetnum).find(rowname).row, self.sheet.get_worksheet(sheetnum).find(colname).col, content)
        return setv

    def setRowData(self, data):
        dataLimit = True
        while dataLimit:
            try:
                self.sheet.get_worksheet(0).insert_row(data, 2)
                dataLimit = False
            except:
                time.sleep(10)
                dataLimit = True