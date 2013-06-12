import ScriptingBridge
import gdata.spreadsheet.service
import time
import shutil

date = 'June 14, 2013'
feed_str = 'tVc9gCzhh-seVwvaojke4Iw'

EShiftDown = 1265854068
ECommandDown = 1264807268
EOptionDown = 1265594484
EControlDown = 1264809068
ELeftArrowKey = 1802730240
ERightArrowKey = 1802730496

pages = ScriptingBridge.SBApplication.applicationWithBundleIdentifier_("com.apple.iwork.pages")
pages.activate()
document = pages.open_('/Users/isaac/Documents/Payout-check-maker.pages')
time.sleep(1)

event = ScriptingBridge.SBApplication.applicationWithBundleIdentifier_("com.apple.systemevents")

def align_right():
    event.keystroke_using_('}', ECommandDown)

def align_left():
    event.keystroke_using_('{', ECommandDown)

def type_out( arg ):
    event.keystroke_using_( arg, 0 )
    newline( 1 )

def select_line():
    event.keystroke_using_( ELeftArrowKey, ECommandDown | EShiftDown )    

def newline( arg ):
    for i in range(arg):
        event.keystroke_using_( "\r", 0 )

def main():
    client = gdata.spreadsheet.service.SpreadsheetsService()
    client.email = 'phoenix@dartoo.com'
    client.password = '3355dartoO'
    client.source = '22K'
    client.ProgrammaticLogin()

    feed = client.GetWorksheetsFeed( feed_str )
    for entry in feed.entry:
        worksheet_id = entry.id.text.rsplit('/',1)[1]
        print worksheet_id + ': ' + entry.title.text
        if entry.title.text == 'Payout':
            break

    rows = client.GetListFeed( feed_str, worksheet_id ).entry
    for row in rows:
        if not row.custom['check'].text: continue
        players = int(row.custom['players'].text)

        division_string = row.custom['division'].text or ''
        divisions = division_string.split()
        if len(divisions) == 0:
            divisions = ['']
        for division in divisions:
            for rank in ['1st', '2nd', '3rd', '4th', '5th-6th', '5th-6th', '7th-8th', '7th-8th']:
                payout = row.custom[ 'rank' + rank ].text
                payout_int = int(payout) / int( row.custom['players'].text )
                payout_str = numToWords( payout_int )
                memo = row.custom['event'].text + ' ' + division + ' on ' + row.custom['day'].text + ' - ' + rank
                for p in range(players):
                    pages.activate()
                    newline( 3 )
                    align_right()
                    type_out( date )
                    newline( 1 )
                    type_out( '***** ' + str(payout_int) + '.00' )
                    newline( 1 )
                    align_left()
                    type_out( '***** ' + payout_str.title() + ' *****' )
                    newline( 4 )
                    type_out( memo )
                    newline( 4 )
                    time.sleep(0.5)





units = ["", "one", "two", "three", "four",  "five", 
    "six", "seven", "eight", "nine "]
teens = ["", "eleven", "twelve", "thirteen",  "fourteen", 
    "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
tens = ["", "ten", "twenty", "thirty", "forty",
    "fifty", "sixty", "seventy", "eighty", "ninety"]
thousands = ["","thousand"]

def numToWords(num):
    words = []
    if num == 0:
        words.append("zero")
    else:
        numStr = "%d" % num
        numStrLen = len(numStr)
        groups = (numStrLen + 2) / 3
        numStr = numStr.zfill(groups * 3)
        for i in range(0, groups*3, 3):
            h = int(numStr[i])
            t = int(numStr[i+1])
            u = int(numStr[i+2])
            g = groups - (i / 3 + 1)
            
            if h >= 1:
                words.append(units[h])
                words.append("hundred")
                
            if t > 1:
                words.append(tens[t])
                if u >= 1:
                    words.append(units[u])
            elif t == 1:
                if u >= 1:
                    words.append(teens[u])
                else:
                    words.append(tens[t])
            else:
                if u >= 1:
                    words.append(units[u])
            
            if g >= 1 and (h + t + u) > 0:
                words.append(thousands[g])
    return ' '.join( words ) 

main()

