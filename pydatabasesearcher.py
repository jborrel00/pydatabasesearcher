import RPi.GPIO as gpio
import serial
import MySQLdb as mdb
from time import sleep
import glob
gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)
gpio.setup(5,gpio.OUT)
gpio.output(5,0)
sleep(.1)
gpio.output(5,1)
sleep(.1)

if '/dev/ttyACM1' in glob.glob('/dev/tty*'):
  ser = serial.Serial('/dev/ttyACM1',115200)
else:
	ser = serial.Serial('/dev/ttyACM0',115200)

s=[]
p=[]
i = 0
con = mdb.connect('localhost','root','foosball','foosball');
with con:
	cur = con.cursor()
	cur.execute('select Id from name_hex_data where [condition]')
	rows = cur.fetchall()
	for row in rows:
		p=row[0] #we should probably only be getting 1 Id at a time
	print p
while i == 0:
	gpio.output(5,0)
	sleep(.1)
	gpio.output(5,1)
	print "reading..."
	for a in range(2):
		r=ser.readline()
		s.append(r)
		print r
	#maybe change this part a bit so that only the Id get stored, instead of Id and side
	if '[Id]' in s:
		print 'exists'
		name ='' #may change this portion as well, alter string formatting of both so make more compatible
		print name
		if name in p:
			print 'EXISTS'
	else:
		gpio.output(5,0)
		sleep(.1)
		gpio.output(5,1)
		sleep(.1)
		gpio.output(5,0)
		sleep(.1)
		gpio.output(5,1)
i=1		
print "done"
