import RPi.GPIO as gpio
import serial
import MySQLdb as mdb
from time import sleep
import glob

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
	cur.execute('select name from name_hex_data')
	rows = cur.fetchall()
	for row in rows:
		p.append(row[0])
	print p
while i == 0:
	gpio.output(5,0)
	sleep(.1)
	gpio.output(5,1)
	print "reading..."
	for a in range(11):
		r=ser.readline()
		s.append(r)
		print r
	if 'Joe\r\n' in s:
		print 'exists'
		name ='Joe'
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
