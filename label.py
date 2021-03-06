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
        sheet = _gdrive.Sheet('22K', 'Label')
        rows = sheet.listfeed.entry
        pages = _pages.Label('/Users/isaac/Documents/', 3)

        pages.key_code( kVK_UpArrow, ECommandDown )
        for row in rows:
            pages.key_code( kVK_DownArrow )
            pages.type_out( row.custom['team'].text )
            time.sleep(0.1)
 
        return "label print done"

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.internalerror = web.debugerror
    app.run()