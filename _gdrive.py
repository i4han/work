import gdata.spreadsheet.service

google_id = 'phoenix@dartoo.com'
password = '3355dartoO'

class Sheet():
    def __init__(__, sheet_name, ):
        __.sheet_name = sheet_name
        __.client = gdata.spreadsheet.service.SpreadsheetsService()
        __.client.email = google_id
        __.client.password = password
        __.client.source = '22K'
        __.client.ProgrammaticLogin()
        __.sheets = client.GetSpreadsheetsFeed()
        __.entry = dict(map(lambda e: (e.title.text, e.id.text.rsplit('/', 1)[1]), sheets.entry))

        __.feed = client.GetWorksheetsFeed( __.entry[ sheet_name ] )
        __.worksheets = dict(map(lambda e: (e.title.text, e.id.text.rsplit('/', 1)[1]),feed.entry))
        __.worksheet = client.GetListFeed( feed__tr, worksheet_id )


        for entry in feed.entry:
            worksheet_id = entry.id.text.rsplit('/',1)[1]
            if entry.title.text == tab:
                break

