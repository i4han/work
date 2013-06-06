#!/usr/bin/python

import ScriptingBridge

COMMAND_KEY = 1264807268
OPTION_KEY = 1265594484

chrome = ScriptingBridge.SBApplication.applicationWithBundleIdentifier_("com.google.chrome")
pages = ScriptingBridge.SBApplication.applicationWithBundleIdentifier_("com.apple.iwork.pages")

pages.activate()

event = ScriptingBridge.SBApplication.applicationWithBundleIdentifier_("com.apple.systemevents")
event.keystroke_using_("123", 0)
event.keystroke_using_("}", COMMAND_KEY)
