# def get_count():
import MySQLdb as db
from get_places import *

if __name__ == '__main__':
	domestic_airports, international_airports = get_airports()
	con = db.connect(host = "localhost", user = "root", passwd = "password")
	cur = con.cursor()
	cur.execute('USE HistoricFlightData;')
	sql = 'CREATE TABLE IF NOT EXISTS passengerCount (flight_no VARCHAR(255), FlightDate DATE,  FlightTime TIME, Origin VARCHAR(255), Destination VARCHAR(255), GateNumber VARCHAR(255), numP DOUBLE);'
	cur.execute(sql);

	airport_name = "HYD"
	sql = 'SELECT * FROM flight_history;'
	

	cur.execute(sql);
	result = cur.fetchall()
	for record in result:
		fno = record[5]
		fdate = str(record[0])
		ftime = str(record[4])
		forig = record[2]
		fdest = record[3]
		if record[2] == "HYD":
			if record[3] in domestic_airports:
				sql = 'SELECT flight_history.flight_no, flight_history.FlightDate, flight_history.FlightTime, flight_history.Origin, flight_history.Destination, flight_history.GateNumber, ((airlinesLoad.domesticLoadFactor*0.01*5) + (dayWeight.domesticWeight*3) + (domesticTraffic.weight*2))*aircraftNoOfSeats.noOfSeats*0.1 AS numP FROM flight_history, airlinesLoad, aircraftNoOfSeats, dayWeight, domesticTraffic WHERE flight_history.airline = airlinesLoad.airline AND flight_history.aircraft = aircraftNoOfSeats.aircraft AND flight_history.airline = aircraftNoOfSeats.airline AND WEEKDAY(flight_history.FlightDate) = dayWeight.dayNo AND flight_history.Origin = "HYD" AND flight_history.flight_no = \"' + fno + '\" AND domesticTraffic.airport = \"' + fdest + '\" AND flight_history.FlightTime = \"' + ftime +  '\" AND flight_history.FlightDate = \"' + fdate + '\";'			
			else:
				continue	
				# sql = 'SELECT flight_history.flight_no, flight_history.FlightDate, flight_history.FlightTime, flight_history.Origin, flight_history.Destination, flight_history.GateNumber, ((airlinesLoad.internationalLoadFactor*0.01*5) + (dayWeight.internationalWeight*3) + (internationalTraffic.weight*2))*aircraftNoOfSeats.noOfSeats*0.1 AS numP FROM flight_history, airlinesLoad, aircraftNoOfSeats, dayWeight, internationalTraffic WHERE flight_history.airline = airlinesLoad.airline AND flight_history.aircraft = aircraftNoOfSeats.aircraft AND flight_history.airline = aircraftNoOfSeats.airline AND WEEKDAY(flight_history.FlightDate) = dayWeight.dayNo AND flight_history.Origin = "HYD" AND flight_history.flight_no = \"' + fno + '\" AND internationalTraffic.airport = \"' + fdest + '\" AND flight_history.FlightTime = \"' + ftime +  '\" AND flight_history.FlightDate = \"' + fdate + '\";'			
			# print sql	

		elif record[3] == "HYD":	
			if record[2] in domestic_airports:
				sql = 'SELECT flight_history.flight_no, flight_history.FlightDate, flight_history.FlightTime, flight_history.Origin, flight_history.Destination, flight_history.GateNumber, ((airlinesLoad.domesticLoadFactor*0.01*5) + (dayWeight.domesticWeight*3) + (domesticTraffic.weight*2))*aircraftNoOfSeats.noOfSeats*0.1 AS numP FROM flight_history, airlinesLoad, aircraftNoOfSeats, dayWeight, domesticTraffic WHERE flight_history.airline = airlinesLoad.airline AND flight_history.aircraft = aircraftNoOfSeats.aircraft AND flight_history.airline = aircraftNoOfSeats.airline AND WEEKDAY(flight_history.FlightDate) = dayWeight.dayNo AND flight_history.Destination = "HYD" AND flight_history.flight_no = \"' + fno + '\" AND domesticTraffic.airport = \"' + forig + '\" AND flight_history.FlightTime = \"' + ftime +  '\" AND flight_history.FlightDate = \"' + fdate + '\";'			
			else:
				continue
				# sql = 'SELECT flight_history.flight_no, flight_history.FlightDate, flight_history.FlightTime, flight_history.Origin, flight_history.Destination, flight_history.GateNumber, ((airlinesLoad.internationalLoadFactor*0.01*5) + (dayWeight.internationalWeight*3) + (internationalTraffic.weight*2))*aircraftNoOfSeats.noOfSeats*0.1 AS numP FROM flight_history, airlinesLoad, aircraftNoOfSeats, dayWeight, internationalTraffic WHERE flight_history.airline = airlinesLoad.airline AND flight_history.aircraft = aircraftNoOfSeats.aircraft AND flight_history.airline = aircraftNoOfSeats.airline AND WEEKDAY(flight_history.FlightDate) = dayWeight.dayNo AND flight_history.Destination = "HYD" AND flight_history.flight_no = \"' + fno + '\" AND internationalTraffic.airport = \"' + forig + '\" AND flight_history.FlightTime = \"' + ftime +  '\" AND flight_history.FlightDate = \"' + fdate + '\";'				

		# print sql

		cur.execute(sql)
		result1 = cur.fetchall()
		
		if result1:
			rec = result1[0]
			# print rec
			sql = 'INSERT INTO passengerCount VALUES (' 
			for r in rec:
				sql += '\"' + str(r) + '\", '
			sql = sql[:-2]	
			sql += ');'	
			# print sql
			cur.execute(sql)

		
	con.commit()
	cur.close()			
