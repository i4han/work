import ScriptingBridge
import shutil


class Pages():
    def __init__(__, url, lines=1):
        __.pages = ScriptingBridge.SBApplication.applicationWithBundleIdentifier_("com.apple.iwork.pages")
        __.pages.activate()
        shutil.copy2( url + 'participants-%1d.pages' % lines, url + 'participants.pages')
        __.document = __.pages.open_( url + 'participants.pages')
        __.event = ScriptingBridge.SBApplication.applicationWithBundleIdentifier_("com.apple.systemevents")

    def type_out(__, arg ):
        __.event.keystroke_using_( arg, 0 )

    def key_code(__, arg, option=0 ):
        __.event.keyCode_using_( arg, option )
