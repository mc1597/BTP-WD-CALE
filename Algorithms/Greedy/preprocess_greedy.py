import csv
import MySQLdb as db
import sys
from flightNode import *
import operator

mapping = {'22' : [], '23' : [], '24' : [], '26' : [], '28': [], '30A' : [], '30B' : [], '25A' : [], '25B' : [], '25C' : []}

def conflictP(gate,flightTime):
	flight_start_time = setStartTime(flightTime,30)
	flight_end_time = setEndTime(flightTime,30)
	for f in mapping[gate]:
		f_start_time = setStartTime(f,30)
		f_end_time = setEndTime(f,30)
		if not(f_start_time > flight_end_time or flight_start_time > f_end_time):
			return True
	return False

def preprocessG(date):
	
	gates = ['22','23','24','26','28','30A','30B','25A','25B','25C']	
	for gate in mapping:
		mapping[gate] = []
	con = db.connect(host = "localhost", user = "root", passwd = "password")
	cur = con.cursor()
	cur.execute('USE HistoricFlightData;')
	
	sql = 'SELECT flight_no,FlightTime,numP FROM passengerCount where FlightDate = \"' + date + '\" AND Origin = \"'+ "HYD" + '\"' + 'GROUP BY FlightTime;'		
	cur.execute(sql);
	records = cur.fetchall()
	fname1 = 'dummydata1.csv'
	file = open(fname1,'wb')
	data = csv.writer(file)
	for r in records:		
		data.writerow([r[0],r[1],int(r[2])])
	file.close()
	


if __name__ == '__main__':
		preprocess(sys.argv[1])
