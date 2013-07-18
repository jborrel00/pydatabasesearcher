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
			s.append(r) #reads output from arduino, including side and card Id
			print r
		#maybe change this part a bit so that only the Id get stored, instead of Id and side
		
		if s in p: #check to see if the card has an Id on file
			print 'exists'
			cur.execute('insert into name_game_data(playerID) values(p)') #this doesn't seem quite right, since we're associating the playerID, not the card Id
			"""name ='' #may change this portion as well, alter string formatting of both so make more compatible
			print name
			if name in p:
				print 'EXISTS'"""
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
