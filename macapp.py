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



def app( indentifier ):
    return ScriptingBridge.SBApplication.applicationWithBundleIdentifier_( indentifier )


class Object():
    def __init__(__):
        __.current_obj = None
    def find(__, obj, name ):
        #print "finding obj: ", name
        for i in obj:
            #print i.name()
            if i.name() == name:
                __.current_obj = i
                return True
        return False

    def get(__):
        return __.current_obj


class Key():
    def __init__(__):
        __.key = app("com.apple.systemevents")

    def home(__):
        __.key_code( UpArrow, CommandDown )

    def newline(__, arg=1 ):
        map(__.type_out( '\r' ), [None] * arg )

    def up(__, arg=1 ):
        map(__.key_code( UpArrow ), [None] * arg )

    def down(__, arg=1 ):
        map(__.key_code( DownArrow ), [None] * arg )

    def page_break(__):
        __.type_out( '\r', ControlDown ) # user defined control-Enter for page break.

    def type_down(__, keys, arg=1 ):
        __.type_out( keys )
        map(__.down(), [None] * arg ) 

    def type_out(__, key, option=0 ):
        __.key.keystroke_using_( key, option )

    def key_code(__, arg, option=0 ):
        __.key.keyCode_using_( arg, option )


class Printer():
    def __init__(__):
        print 'key init'
        __.print_app = app("com.apple.print.PrintCenter")
        __.currentPrinter = __.print_app.currentPrinter()
        __.default = __.currentPrinter
        __.printers = __.print_app.printers()

    def current(__, name='' ):
        if name:
            for i in __.printers:
                if i.name() == name:
                    __.app.setCurrentPrinter_(i)
                    __.currentPrinter = __.print_app.currentPrinter()
        return __.currentPrinter

    def default(__):
        __.app.setCurrentPrinter_( __.default )




class Label( Key ):
    def __init__(__, url, lines=1):
        Key.__init__(__)
        __.pages = app("com.apple.iwork.pages")
        __.pages.activate()
        shutil.copy2( url + 'participants-%1d.pages' % lines, url + 'participants.pages')
        __.document = __.pages.open_( url + 'participants.pages')


class Check( Key ):
    def __init__(__, url):
        Key.__init__(__)
        __.pages = app("com.apple.iwork.pages")
        __.pages.activate()
        shutil.copy2( url + 'check-one.pages', url + 'check_temp.pages')
        __.document = __.pages.open_( url + 'check_temp.pages')
        __.pages.activate()

    def activate(__):
        __.pages.activate()


class Pages( Key, Printer ):
    def __init__(__):
        Key.__init__(__)
        __.app = app("com.apple.iwork.pages")
        __.app.activate()
        __.documents = __.app.documents().get()

    def document__(__, name):
        __.document = find(__.documents, name)

        
        p = i.bodyText().paragraphs()[0]
        print p.text()[2].get()
        i.bodyText().paragraphs()[1].setTo_('This is it\n')
        print '=' * 100

    def print__(__):
        __.app.print_printDialog_withProperties_(i, False, None)

    def activate(__):
        __.app.activate()



class Cell():
    def __init__(__, cell):
        __.cell = cell

    def value(__, value=None):
        if value:
            __.cell.setValue_( value )
        properties = __.cell.properties()
        return properties['value']

    def address(__):
        return __.cell.properties()['address']



class Column():
    def __init__(__, column):
        __.column = column

    def value(__, value=None):
        if value:
            __.cell.setValue_( value )
        properties = __.cell.properties()
        return properties['value']


def column_name( column ):
    ascii = ord('A')
    digit2 = chr( ascii + column / 26 % 26 - 1) if column > 25 else '' 
    digit1 = chr( ascii + column % 26 )
    return digit2 + digit1


class Numbers( Key ):
    def __init__(__):
        Key.__init__(__)
        __.obj = Object()
        __.app = app("com.apple.iwork.numbers")
        #__.app.activate()
        __.documents = __.app.documents().get()
        __.current_document = None
        __.current_sheet = None
        __.current_table = None
        __.current_cell = None
        

    def document(__, name='' ):
        if __.obj.find( __.documents, name):
            __.current_document = __.obj.get()
            __.sheets = __.current_document.sheets().get()
            return __

    def sheet(__, name):
        if __.obj.find( __.sheets, name):
            __.current_sheet = __.obj.get()
            __.tables = __.current_sheet.tables().get()
            return __

    def table(__, name):
        if __.obj.find(__.tables, name):
            __.current_table = __.obj.get()
            __.cells = __.current_table.cells().get()
            __.rows  = __.current_table.rows().get()
            __.columns = __.current_table.columns().get()
            return __

    def row(__, name):
        if __.obj.find(__.rows, name):
            __.current_row = __.obj.get()
            __.cells = __.current_row.cells().get()
            return __

    def column(__, name):
        if type( name ) == int:
            name = column_name( name )
        print name
        if __.obj.find(__.columns, name):
            __.current_column = __.obj.get()
            __.cells = __.current_column.cells().get()
            return __

    def cell(__, name):
        if __.obj.find(__.cells, name):
            __.current_cell = __.obj.get()
            __.Cell = Cell( __.current_cell )
            return __

    def offset(__, row, column):
        return __.cell( column_name( column ) + str( row + 1 ) )

    def value(__, row, column):
        __.offset( row, column )
        return __.Cell.value()




class iTunes( Key ):
    def __init__(__):
        Key.__init__(__)
        __.app = app("com.apple.itunes")
        __.app.activate()


class Chrome( Key ):
    def __init__(__):
        Key.__init__(__)
        __.app = app("com.google.chrome")
        __.app.activate()
        __.windows = __.app.windows().get()
        __.tabs = __.window[-1].tabs()
        __.tab = __.tabs[-1]

    def url(__, location ):
        __.tab.setURL_( location )

    def javascript(__, source ):
        __.tab.executeJavascript_( source )

    def selectAll(__):
        __.tab.selectAll()

    def copy(__):
        __.tab.copySelection()

    def viewSource(__):
        __.tab.viewSource()

def dirs( obj ):
    print (list(set(dir( obj )) - set(dir( ScriptingBridge.SBObject ))))


if __name__ == '__main__':
    n = Numbers()
    n.document('Untitled 21').sheet('Sheet 1').table('Table 1')
    n.cell('C2')
    print n.current_table
    dirs( n.current_cell )


    n.Cell.value('Hello World')
    print n.Cell.value() 


#    p = Printer()
#    print p.current().name()
#    print p.current('brother_ql-700@krypton').name()



