#!/usr/bin/python

import ScriptingBridge
import os
import sys

pages = ScriptingBridge.SBApplication.applicationWithBundleIdentifier_("com.apple.iWork.pages")
pages.activate()
document = pages.open_('/Users/isaac/Documents/participants.pages')
text = document.bodyText()
print text

characters = text.characters()
words = text.words()
context = text.context()
get = text.get()
paragraphs = text.paragraphs()
for i in dir(paragraphs):
    print i
# paragraphs.removeAllObjects()
paragraphs.insertString_BU_atIndex_("hello", 1)
array = paragraphs.get()

print array

