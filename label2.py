import web
import _gdrive
import _pages
import time

EShiftDown   = 1265854068
ECommandDown = 1264807268
EOptionDown  = 1265594484
EControlDown = 1264809068
kVK_LeftArrow  = 0x7B
kVK_RightArrow = 0x7C
kVK_DownArrow  = 0x7D
kVK_UpArrow    = 0x7E

urls = (
    '/', 'index'
)

class index:
    def GET(self):
        sheet = _gdrive.Sheet('22K', 'Blind')
        rows = sheet.listfeed.entry
        lines = 2 if rows[0].custom['team'].text.find(',') else 2
        pages = _pages.Label('/Users/isaac/Documents/', lines)

        pages.key_code( kVK_UpArrow, ECommandDown )
        for row in rows:
            pages.type_out( row.custom['number'].text )
            pages.key_code( kVK_DownArrow )
            if lines == 2:
                team1, team2 = row.custom['team'].text.split(',')
                pages.type_out( team1 )
                pages.key_code( kVK_DownArrow ) 
                pages.type_out( team2 )
                time.sleep(0.1)
            else:
                pages.type_out( row.custom['team'].text )
            pages.key_code( kVK_DownArrow ) 

        return "label print done"

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.internalerror = web.debugerror
    app.run()