import web
import _gdrive
import _pages
import time


class Main:
    def __init__(self, sheet_name, lines=1):
        sheet = _gdrive.Sheet('22K', 'lady_doubles_final')
        rows = sheet.listfeed.entry
        pages = _pages.Label('/Users/isaac/Documents/', lines)
        pages.home()
        for row in rows:
            pages.down()
            team = row.custom['team'].text
            pages.type_out( team )
            pages.type_out( "\r" )
            pages.down()
            print team
            time.sleep(0.1)
 

if __name__ == "__main__": Main( 'lady_doubles_final', 1)
