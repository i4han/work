import gdata.spreadsheet.service
import ScriptingBridge
import time
import sys
import psycopg2

EShiftDown   = 1265854068
ECommandDown = 1264807268
EOptionDown  = 1265594484
EControlDown = 1264809068
kVK_LeftArrow  = 0x7B
kVK_RightArrow = 0x7C
kVK_DownArrow  = 0x7D
kVK_UpArrow    = 0x7E


conn = psycopg2.connect(database ='djangostack',host='dev.dartoo.com',port='5432',user='postgres', password='tnvkfdl2')
pages = ScriptingBridge.SBApplication.applicationWithBundleIdentifier_("com.apple.iwork.pages")
pages.activate()
document = pages.open_('/Users/isaac/Documents/participants-1-line.pages')
pages.saveAs_in_("SLDocumentTypeRichText", rtfDocFilePath)
event = ScriptingBridge.SBApplication.applicationWithBundleIdentifier_("com.apple.systemevents")
#event.keystroke_using_('p', ECommandDown)
#time.sleep(1)
#event.keystroke_using_("\r", 0)

#sys.exit()

class Pages():
    def __init__(__):

def type_out( arg ):
    event.keystroke_using_( arg, 0 )

def key_code( arg, option=0 ):
    event.keyCode_using_( arg, option )




class Gsheet22k():
    def __init__(__, tab ):
        __.tab = tab
        client = gdata.spreadsheet.service.SpreadsheetsService()
        client.email = 'phoenix@dartoo.com'
        client.password = '3355dartoO'
        client.source = '22K'
        client.ProgrammaticLogin()

        feed__tr = 'tVc9gCzhh-seVwvaojke4Iw'
        feed = client.GetWorksheetsFeed( feed__tr )
        for entry in feed.entry:
            worksheet_id = entry.id.text.rsplit('/',1)[1]
            if entry.title.text == tab:
                break

        __.feed = client.GetListFeed( feed__tr, worksheet_id )



#@unused
class Player():
    def __init__(__, name, stats=0.0, mobile='' ):
        __.name = name
        __.stats = stats
        __.mobile = mobile



#@unused
class Team():
    def __init__(__, id, team_name ):
        __.id = id
        __.team_name = team_name
        __.players = []

    def append(__, player_name, ranking ):
        __.players.append( Player( player_name ) )



class Match():
    def __init__(__, id, round, ranking, winners_go, losers_go ):
        __.id = id
        __.round = round
        __.ranking = ranking
        __.winner = None
        __.loser = None
        __.winners_go = winners_go
        __.losers_go = losers_go
        __.teams = []
        __.status = ''

    def assign(__, id ):
        __.teams.append( id )        



class Division():
    def __init__(__, name, format, teams ):
        __.format = format
        __.name = name
        __.teams = teams
        __.match = [None] * 129
        __.seed = [None] * 65
        __.team_numbers = len( teams ) 
        __.byes = 64 - __.team_numbers
        __.bye = __.team_numbers + 1
        if __.byes:
            __.teams[ str(__.team_numbers + 1) ] = 'bye'

        sheet = Gsheet22k( 'Bracket' )
        rows = sheet.feed.entry
        for row in rows:
            id = int( row.custom['id'].text )
            __.match[id] = Match( id=id,
                round= int( row.custom['round'].text ),
                ranking= row.custom['ranking'].text,
                winners_go= int( row.custom['winners-go'].text or 0 ),
                losers_go= int( row.custom['losers-go'].text or 0 ) )

            seed1 = int( row.custom['seed1'].text or 0 )
            if seed1: __.seed[ seed1 ] = id
            seed2 = int( row.custom['seed2'].text or 0 )
            if seed2: __.seed[ seed2 ] = id
        print teams
        __.seeding( teams )
        __.put_byes()


    def seeding(__, teams):
        for position in teams:
            team_name = teams[ position ]
            position = int( position )
            if position <= 32:
                id =  __.seed[ position ]
                __.match[ id ].assign( position ) 
            elif team_name != 'bye':
                id = __.seed[ position + __.byes ]
                __.match[ id ].assign( position ) 

    def put_byes(__):
        for row in range(1,33):
            if len( __.match[ row ].teams ) < 2:
                __.match[ row ].teams.append( __.bye )

    def round(__):
        for row in __.match:
            if ( row and row.winners_go and row.status != 'completed' and len( row.teams ) == 2 ):
                # who is winner
                __.match[ row.id ].teams.sort()
                winner_id = __.match[ row.id ].teams[0]
                __.report_match( row.id, winner_id )

    def report_match(__, match_id, winner_id ):
            __.match[ match_id ].status = 'completed'
            teams =  __.match[ match_id ].teams[:]
            teams.remove( winner_id )
            loser_id = teams.pop()
            print match_id, ':', winner_id, loser_id
            winners_go = __.match[ match_id ].winners_go
            __.match[ winners_go ].assign( winner_id )
            losers_go = __.match[ match_id ].losers_go
            if losers_go:
                __.match[ losers_go ].assign( loser_id )
            #release console


    def write(__):
        print __.teams
        for row in __.match:
            if row and row.teams:
                print row.id, ':', row.round, row.teams, row.ranking
        key_code( kVK_UpArrow, ECommandDown )
        for i in range(1, 33):
            for j in range(0, 2):
                position = __.match[i].teams[j]     
                type_out( '%03d%02d%03d' % ( i, 1, position ) )
                key_code( kVK_DownArrow )
                type_out( __.teams[ str(position) ] )
                key_code( kVK_DownArrow ) 



#class Event():
#    def __init__(__, players ):
        

#               int(row.teams[1]) - int(row.teams[0])


def main():
    sheet = Gsheet22k( 'Gold' )
    rows = sheet.feed.entry
    teams = {}
    for row in rows:
        teams[ row.custom['id'].text ] = row.custom['team'].text

    division = Division( 'Gold', 'Singles', teams )
    division.write()
    division.round()



main()