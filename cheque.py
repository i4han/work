import web
import _gdrive
import _pages
import time
import sys

class Main:
    def __init__(__):
        date = 'August 16, 2013'
        check_number = 220001

        pages = _pages.Check('/Users/isaac/Documents/')
        sheet = _gdrive.Sheet('22K', 'Payout')
        rows = sheet.listfeed.entry
        time.sleep(2)
        pages.home()
        for row in rows:
            print row.custom['event'].text
            if not row.custom['check'].text: continue
            players = int(row.custom['players'].text)
            division_string = row.custom['division'].text or ''
            divisions = division_string.split()
            if len(divisions) == 0:
                divisions = ['']
            for division in divisions:
                for rank in ['1st', '2nd', '3rd', '4th', '5th-6th', '5th-6th', '7th-8th', '7th-8th']:
                    payout = row.custom[ 'rank' + rank ].text
                    if not payout: continue
                    payout_int = int(payout) / int( row.custom['players'].text )
                    payout_per_winner = "{:,}".format( payout_int )
                    payout_str = numToWords( payout_int )
                    event_name = row.custom['event'].text + ' ' + division
                    for p in range(players):
                        pages.activate()
                        pages.type_down( str(check_number) )
                        pages.type_down( date )
                        pages.type_down( '$' + payout_per_winner + '.00' )
                        pages.type_down( '***** ' + payout_str.title() + ' *****' )
                        time.sleep(0.5)
                        pages.type_down( event_name )
                        pages.type_down( rank )
                        pages.type_down( 'c' + str(check_number) + 'c', 2 )
                        time.sleep(0.5)
                        pages.type_down( event_name )
                        pages.type_down( rank )
                        pages.type_down( '$' + payout_per_winner )
                        pages.type_down( '$' + "{:,}".format( int( payout ) ), 2 )

                        check_number += 1
                        time.sleep(0.5)



units = ["", "one", "two", "three", "four",  "five", "six", "seven", "eight", "nine "]
teens = ["", "eleven", "twelve", "thirteen",  "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
tens = ["", "ten", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
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

if __name__ == "__main__": Main()

