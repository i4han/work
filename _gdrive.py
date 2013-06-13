import gdata.spreadsheet.service

google_id = 'phoenix@dartoo.com'
password = '3355dartoO'

class Sheet():
    def __init__(__, book_name, sheet_name):
        __.book_name = book_name
        __.sheet_name = sheet_name

        __.client = gdata.spreadsheet.service.SpreadsheetsService()
        __.client.email = google_id
        __.client.password = password
        __.client.ProgrammaticLogin()

        __.workbooks = __.client.GetSpreadsheetsFeed()
        __.workbook = dict(map(lambda e: (e.title.text, e.id.text.rsplit('/', 1)[1]), __.workbooks.entry))
        __.key = __.workbook[ book_name ]

        __.sheets = __.client.GetWorksheetsFeed( __.key )
        __.sheet = dict(map(lambda e: (e.title.text, e.id.text.rsplit('/', 1)[1]), __.sheets.entry))
        __.sheet_id = __.sheet[ sheet_name ]

        __.listfeed = __.client.GetListFeed( __.key, __.sheet_id )

    def insert(__, row_data={}):
        __.client.InsertRow( row_data=row_data, key=__.key, wksht_id=__.sheet_id)
    def delete(__, row=0):
        __.client.DeleteRow( __.listfeed.entry[ row ])
    def delete_all(__):
        for i in range(len(__.listfeed.entry) - 1, -1, -1):
            __.delete( i )

"""
def getRows(self):
                       return self.gd_client.GetListFeed(key=self.key,wksht_id=self.wksht_id).entry
                   def insertRow(self,row_data):
                       return self.gd_client.InsertRow(row_data,key=self.key,wksht_id=self.wksht_id)
                   def deleteRow(self,entry):
                       return self.gd_client.DeleteRow(entry)
                   def deleteAllRows(self):
                       entrylist = self.getRows()
                       i = 0
                       for entry in entrylist:
                           self.deleteRow(entry)
                           i += 1
                           print "deleted row ", i

"""