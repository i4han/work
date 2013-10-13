import re
import time
from datetime import datetime
import sys
import applescript
import dmx
import pickle
import macapp
import lightshow

script = applescript.AppleScript("""
    on play(song)
    	tell application "iTunes"
			play track song
		end tell
    end
""")

def playsong( song ):
	script.call('play', song )

class Light():
	def __init__(__):
		__.dmxman = dmx.DMXManager('/dev/cu.usbserial-EN137673')
		__.light = {}
		__.address = {}
		__.inter = {}

	def add_light(__, id, start, length ):
		device = dmx.DMXDevice(start=start, length=length)
		__.dmxman.append( device )
		__.light[ str(id) ] = device
		# print 'add light:', str(id)

	def add_address(__, name, id, address):
		name = str( name )
		__.address[ name ] = {}
		__.address[ name ][ 'id' ] = id
		__.address[ name ][ 'address' ] = address

	def print_light(__, id):
		pass
		# print "Light", id, __.light[ str(id) ]

	def send(__, name, value ):
		name = str(name)
		# print 'sending:', name, ' value:', value
		__.light[ str(__.address[name]['id']) ].set( __.address[name]['address'], value)
		__.address[ name ]['value'] = value
		# print 'sending:', __.address[name]['id'],  __.address[name]['address'], value
	def send_direct(__, light):
		for l in light:
			__.light[ l[0] ].set( l[1], l[2] )

	def send_dmx(__):
		__.dmxman.send()

	def sendline(__, dct ):
		if 'beat' in dct:
			dct.pop('beat')
		if dct != None:
			for key in dct:
				# print 'key:', key, str(__.address[ key ]['id']), __.address[ key ]['address'], dct[ key ]
				# print '', __.light[ str(__.address[ key ]['id']) ]
				__.light[ str(__.address[ key ]['id']) ].set( __.address[ key ]['address'], dct[ key ])
				__.dmxman.send()
			
	def line(__, dct ):
		light_line = []
		if dct != None:
			for key in dct:
				if key == 'beat':
					continue
				light_line.append([str(__.address[ key ]['id']), __.address[ key ]['address'], dct[ key ] ])
		return light_line
			
			

def main():
	l = Light()

	if 1:
		file = open('Summer.lshow', 'rb')
		Show = pickle.load( file )
	else:
		Show = lightshow.prepare()

	n_lights = Show['n_lights']
	n_addresses = Show['n_addresses']
	n_lines = Show['n_lines']
	bpm = Show['bpm']
	timing = 0
	for i in range( 1, n_lights + 1):
		point = Show['light'][i]
		l.add_light( id=i, start=point['start'], length=point['length'] )
	for i in range( 0, n_addresses ):
		point = Show['address'][i]
		print 'point:', point
		l.add_address( name=point['name'], id=point['id'], address=point['address'] )
	for i in range( 1, n_lights + 1):
		l.print_light( i )



	Play = []
	for line in Show['timeline']:
		print line
		beat = line['beat']
		timing += beat 
		Play.append({'timing': float(timing), 'send': l.line( line )})

	print 'Lines:', len(Show['timeline'])
	print 'Play:', Play
	
	l.send_direct( Play[0]['send'] )
	playsong('Summer')
	start = datetime.now()
	for i in range(1, len(Play)):
		l.send_dmx()
		l.send_direct( Play[i]['send'] )
		delta = datetime.now() - start
		lapse = delta.seconds + delta.microseconds / 1000000.
		delay = max(  Play[i-1]['timing'] / bpm - lapse, 0 )
		time.sleep( delay )







if __name__ == '__main__':
	main()