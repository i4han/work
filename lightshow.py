import re
import pickle
import macapp

isfloat = re.compile('^[0-9.]+$')

start_column = 3

def value(cell):
	ret = macapp.Cell(cell).value()
	ret = '{}'.format( ret )
	if ret == '0.0':
		return ''
	elif ret == '*':
		return 0
	elif ret == '^' or ret == '/':
		return ''
	if isfloat.match( ret ):
		ret = int( float( ret ) )
	return ret

def prepare():
	Show = {}
	n = macapp.Numbers()
	summary = n.document('Lightshow').sheet('Summary').table('Show1')
	n.column('A')
	sheet_name = value( n.cells[0] )
	Show['song'] = value( n.cells[1] )
	Show['bpm'] = value( n.cells[5] )	
	Show['n_lights'] = n_lights = value( n.cells[2] )
	Show['n_addresses'] = n_addresses = value( n.cells[3] )
	Show['n_lines'] = n_lines = value( n.cells[4] )
	Show['timeline'] = []
	Show['light'] = [None] * ( n_lights + 1 )
	Show['address'] = [{}]

	sheet = n.document('Lightshow').sheet(sheet_name)

	sheet.table('Set')
	for i in range(start_column, n_addresses + start_column):
		n.column(i)
		if value( n.cells[0] ):
			id = value(n.cells[0])
			Show['light'][id] = {}
			Show['light'][id]['start'] = value(n.cells[1])
			Show['light'][id]['length'] = value(n.cells[2])
		if value( n.cells[4] ) != '':
			Show['address'].append({})
			Show['address'][i-start_column]['name'] = str(n.cells[4].column().name())
			Show['address'][i-start_column]['id'] = id
			Show['address'][i-start_column]['address'] = value(n.cells[4])

	sheet.table('Timeline')
	beat_sum = 0 
	i = -1
	repeat = {}
	repeat['mode'] = False
	repeat['timeline'] = {}

	def record( timeline, end=False ):
		print 'repeat():', repeat['mode'], repeat['end'], end
		if timeline != None:
			if repeat['mode']:
				repeat['timeline'][ repeat[ 'rhythm_name' ] ].append( timeline )
			else:
				Show['timeline'].append( timeline )
				print len( Show['timeline'] )
		if repeat['end'] and end:
			Show['timeline'].extend( repeat['timeline'][ repeat[ 'rhythm_name' ] ] * repeat['times'] )
			print len( Show['timeline'] )
			repeat['mode'] = False
			repeat['end'] = False
			repeat['times'] = None

	for row in n.rows:
		print '\n' + str( i ),
		i += 1
		timeline = {}

		cells = row.cells().get()
		beat = value(cells[start_column - 1])
		if beat == '':
			break
		repeat['end'] = False
		__repeat = value(cells[start_column - 2])
		if isinstance(__repeat, int) and __repeat > 0:
			print 'repeat:', __repeat , 'times'
			repeat['mode'] = True
			repeat['beat'] = beat
			repeat['times'] = __repeat
			rhythm_name = str(value(cells[start_column - 3]))
			if rhythm_name:
				repeat['rhythm_name'] = rhythm_name
				if beat == 0:
					print 'Repeat', rhythm_name, repeat['times']
					repeat['end'] = True
					record( None, end=True )
				else:
					print 'Define Repeat', rhythm_name, repeat['times']
					repeat['timeline'][ repeat['rhythm_name'] ] = []
			else:
				repeat['rhythm_name'] = 'default'
				repeat['timeline']['default'] = []

		elif __repeat == ':||':
			print 'end repeat'
			repeat['end'] = True
		variation = False
		print 'beat:', beat
		expend = {}
		for cell in cells[start_column:]:
			cell_value = value( cell )
			key = str(cell.column().name())
			if len(str(cell_value)) > 0:
				print  key + '[' + str( cell_value ) + ']',
			if cell_value != '':
				if isinstance(cell_value, str) and cell_value.find('-') > 0:
					variation = True
					start, end = cell_value.split('-')
					expend[key] = {}
					expend[key]['value'] = float( start )
					expend[key]['end'] = float( end )
					expend[key]['increase'] = ( float( end ) - float( start ) ) / ( beat - 1 )
					cell_value = int( start )
				timeline[key] = cell_value
		if variation:
			timeline['beat'] = 1
			record( timeline )
			for j in range(2, beat):
				timeline = {}
				for key in expend:
					expend[key]['value'] += expend[key]['increase'] 
					timeline[key] = int( expend[key]['value'] )
				timeline['beat'] = 1
				record( timeline )
			timeline = {}
			for key in expend:
				timeline[key] = int( expend[key]['end'] )
			timeline['beat'] = 1
			record( timeline, end=True )
		else:
			timeline['beat'] = beat
			record( timeline, end=repeat['end'] )
		print i, len(Show['timeline'])


	print len(Show['timeline']), 'lines'

	file =open(sheet_name + '.lshow', 'wb')
	pickle.dump(Show, file)
	file.close()

	return Show


if __name__ == '__main__':
	prepare()

