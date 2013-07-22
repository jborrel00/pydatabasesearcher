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
	cur.execute('select Id from name_hex_data')
	rows = cur.fetchall()
	for row in rows:
		p=p.append(row[0]) #gathers all Ids from name_hex_data
	print p
	
	while i == 0:
		gpio.output(5,0)
		sleep(.1)
		gpio.output(5,1)
		print "reading..."
		for a in range(2):
			r=ser.readline()
			s.append(r.rstrip()) #reads output from arduino, including side - s[0] -  and card Id - s[1]
			print int(r,16)
			s = int(s[1],16)
				
		if s[1] in p: #check to see if the card has an Id on file
			print 'exists in name_hex_data'
			cur.execute('update current_card set current_ID = '+s)
			
		else:
			gpio.output(5,0)
			sleep(.1)
			gpio.output(5,1)
			sleep(.1)
			gpio.output(5,0)
			sleep(.1)
			gpio.output(5,1)
	i=1 #may attach to positive if section only so that the code keeps looping until it finds what it wants		
print "done"
