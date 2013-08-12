import ScriptingBridge
import shutil
import time

ShiftDown   = 1265854068
CommandDown = 1264807268
OptionDown  = 1265594484
ControlDown = 1264809068
LeftArrow   = 0x7B
RightArrow  = 0x7C
DownArrow   = 0x7D
UpArrow     = 0x7E
KeyC = 8

class Document():
    def __init__(__):
        __.event = ScriptingBridge.SBApplication.applicationWithBundleIdentifier_("com.apple.systemevents")

    def align_right(__):
        __.type_out('}', CommandDown)

    def align_left(__):
        __.type_out('{', CommandDown)

    def newline(__, arg=1 ):
        for i in range(arg):
            __.type_out( '\r' )

    def home(__):
        __.key_code( UpArrow, CommandDown)
#        __.type_out( RightArrow, CommandDown)

    def up(__, arg=1 ):
        for i in range(arg):
            __.key_code( UpArrow )


    def down(__, arg=1 ):
        for i in range(arg):
            __.key_code( DownArrow )

    def page_break(__):
        __.type_out( '\r', ControlDown) # user defined control-Enter for page break.

    def type_down(__, keys, arg=1 ):
        __.type_out( keys )
        for i in range(arg):
            __.down()

    def type_out(__, key, option=0 ):
        __.event.keystroke_using_( key, option )

    def key_code(__, arg, option=0 ):
        __.event.keyCode_using_( arg, option )

    def select_line():
        __.key_code( LeftArrow, CommandDown | ShiftDown )    

    def copy(__):
        __.key_code( KeyC, CommandDown)

    def paste(__):
        __.type_out( 'v', CommandDown)

    def copy_all(__):
        __.home()
        __.key_code( DownArrow, CommandDown )
        __.key_code( UpArrow, CommandDown | ShiftDown)
        time.sleep(1)
        __.copy()


class Label( Document ):
    def __init__(__, url, lines=1):
        Document.__init__(__)
        __.pages = ScriptingBridge.SBApplication.applicationWithBundleIdentifier_("com.apple.iwork.pages")
        __.pages.activate()
        shutil.copy2( url + 'participants-%1d.pages' % lines, url + 'participants.pages')
        __.document = __.pages.open_( url + 'participants.pages')


class Check( Document ):
    def __init__(__, url):
        Document.__init__(__)
        __.pages = ScriptingBridge.SBApplication.applicationWithBundleIdentifier_("com.apple.iwork.pages")
        __.pages.activate()
        shutil.copy2( url + 'check-one-page.pages', url + 'check_temp.pages')
        __.document = __.pages.open_( url + 'check_temp.pages')

    def activate(__):
        __.pages.activate()

class Check( Document ):
    def __init__(__, url):
        Document.__init__(__)
        __.pages = ScriptingBridge.SBApplication.applicationWithBundleIdentifier_("com.apple.iwork.pages")
        __.pages.activate()
        shutil.copy2( url + 'check-one-page.pages', url + 'check_temp.pages')
        __.document = __.pages.open_( url + 'check_temp.pages')

    def activate(__):
        __.pages.activate()



