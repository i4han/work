import ScriptingBridge
import shutil

ShiftDown   = 1265854068
CommandDown = 1264807268
OptionDown  = 1265594484
ControlDown = 1264809068
LeftArrow   = 0x7B
RightArrow  = 0x7C
DownArrow   = 0x7D
UpArrow     = 0x7E


class Label():
    def __init__(__, url, lines=1):
        __.pages = ScriptingBridge.SBApplication.applicationWithBundleIdentifier_("com.apple.iwork.pages")
        __.pages.activate()
        shutil.copy2( url + 'participants-%1d.pages' % lines, url + 'participants.pages')
        __.document = __.pages.open_( url + 'participants.pages')
        __.event = ScriptingBridge.SBApplication.applicationWithBundleIdentifier_("com.apple.systemevents")

    def home(__):
        __.type_out( UpArrow, CommandDown)
        __.type_out( RightArrow, CommandDown)
        
    def down(__):
        __.type_out( DownArrow )        
    def type_out(__, key, option=0 ):
        __.event.keystroke_using_( key, option )

    def key_code(__, arg, option=0 ):
        __.event.keyCode_using_( arg, option )
