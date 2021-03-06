import datetime
import MySQLdb as db
from datetime import datetime
from get_places import *

domestic_airports, international_airports = get_airports()

def get_parameters():
	parameters = {}
	airlines = {}
	airlines['6E'] = {'domestic' : 85.1, 'international' : 0}
	airlines['SG'] = {'domestic' : 90.1, 'international' : 0}
	airlines['G8'] = {'domestic' : 87.5, 'international' : 0}
	airlines['AI'] = {'domestic' : 88.7, 'international' : 86.7}
	airlines['UK'] = {'domestic' : 79.6, 'international' : 86.7}
	airlines['9W'] = {'domestic' : 84.8, 'international' : 0}
	airlines['I5'] = {'domestic' : 0, 'international' : 0}
	airlines['2T'] = {'domestic' : 0, 'international' : 0}
	airlines['EK'] = {'domestic' : 0, 'international' : 86.7}
	airlines['EY'] = {'domestic' : 0, 'international' : 86.7}
	airlines['MI'] = {'domestic' : 0, 'international' : 86.7}
	airlines['AK'] = {'domestic' : 0, 'international' : 86.7}
	airlines['MH'] = {'domestic' : 0, 'international' : 86.7}
	airlines['TG'] = {'domestic' : 0, 'international' : 86.7}
	airlines['TR'] = {'domestic' : 0, 'international' : 86.7}
	airlines['CX'] = {'domestic' : 0, 'international' : 86.7}
	airlines['FZ'] = {'domestic' : 0, 'international' : 86.7}
	airlines['QR'] = {'domestic' : 0, 'international' : 86.7}
	airlines['G9'] = {'domestic' : 0, 'international' : 86.7}
	airlines['BA'] = {'domestic' : 0, 'international' : 86.7}
	airlines['GF'] = {'domestic' : 0, 'international' : 86.7}
	airlines['SV'] = {'domestic' : 0, 'international' : 86.7}
	airlines['WY'] = {'domestic' : 0, 'international' : 86.7}
	
	parameters['airlines'] = airlines

	aircrafts = {}
	aircrafts['A320'] = {'6E' : 180, 'G8' : 180, 'I5' : 180, 'UK' : 144, 'MI' : 150, 'EY' : 136, 'AI' : 168}
	aircrafts['A319'] = {'AI' : 144}
	aircrafts['737'] = {'SG' : 189}
	aircrafts['A321'] = {'AI' : 182, 'EY' : 174}
	aircrafts['DH8B'] = {'SG' : 50}
	aircrafts['B738'] = {'9W' : 170, 'SG' : 189, 'MI' : 162}
	aircrafts['B77W'] = {'AI' : 342}
	aircrafts['B77L'] = {'AI' : 238}
	aircrafts['B737'] = {'9W' : 134}
	aircrafts['AT72'] = {'9W' : 72}
	aircrafts['B739'] = {'9W' : 189}
	aircrafts['B773'] = {'SV' : 413}
	aircrafts['B772'] = {'SV' : 341}
	aircrafts['777'] = {'SV' : 305}
	parameters['aircrafts'] = aircrafts

	days = {}
	days[0] = {'domestic' : 0.8, 'international' : 0.8}
	days[1] = {'domestic' : 0.75, 'international' : 0.7}
	days[2] = {'domestic' : 0.75, 'international' : 0.7}
	days[3] = {'domestic' : 0.8, 'international' : 0.8}
	days[4] = {'domestic' : 0.85, 'international' : 0.9}
	days[5] = {'domestic' : 0.75, 'international' : 0.7}
	days[6] = {'domestic' : 0.85, 'international' : 0.9}	
	parameters['days'] = days
	return parameters


def populate_domestic_db():
	parameters = get_parameters()
	
	con = db.connect(host = "localhost", user = "root", passwd = "password")
	cur = con.cursor()
	cur.execute('USE HistoricFlightData;')

	cur.execute('CREATE TABLE IF NOT EXISTS airlinesLoad (airline VARCHAR(255), domesticLoadFactor VARCHAR(255), internationalLoadFactor VARCHAR(255));')
	for airline in parameters['airlines']:
		sql = 'INSERT INTO airlinesLoad VALUES('
		sql += '\"' + airline + '\"' + ',' + '\"' + str(parameters['airlines'][airline]['domestic']) + '\"' + ',' + '\"' + str(parameters['airlines'][airline]['international']) + '\"' + ');'
		cur.execute(sql)

	cur.execute('CREATE TABLE IF NOT EXISTS dayWeight(dayNo INT, domesticWeight DOUBLE, internationalWeight DOUBLE);')
	for day in parameters['days']:
		sql = 'INSERT INTO dayWeight VALUES('
		sql += str(day) + ',' + str(parameters['days'][day]['domestic'])  + ',' + str(parameters['days'][day]['international']) + ');'
		cur.execute(sql)
	
	cur.execute('CREATE TABLE IF NOT EXISTS specialDays(specialDate DATE, factor DOUBLE);')
	#add the special dates and corresponding weights

	cur.execute('CREATE TABLE IF NOT EXISTS aircraftNoOfSeats (aircraft VARCHAR(255), airline VARCHAR(255), noOfSeats INT);')
	for aircraft in parameters['aircrafts']:
		for airline in parameters['aircrafts'][aircraft]:
			sql = 'INSERT INTO aircraftNoOfSeats VALUES ('
			sql += '\"' + aircraft + '\"' + ',' + '\"' + airline + '\"' + ',' + str(parameters['aircrafts'][aircraft][airline]) + ');'
			cur.execute(sql)

	traffic_airports = get_traffic('HYD', domestic_airports, 200, 400)
	cur.execute('CREATE TABLE IF NOT EXISTS domesticTraffic(airport VARCHAR(255), weight DOUBLE);')
	for airport in traffic_airports['high_traffic']:
		sql = 'INSERT INTO domesticTraffic VALUES('
		sql += '\"' + airport + '\"' + ',' + str(0.9) + ');'
		cur.execute(sql)
	for airport in traffic_airports['medium_traffic']:
		sql = 'INSERT INTO domesticTraffic VALUES('
		sql += '\"' + airport + '\"' + ',' + str(0.85) + ');'
		cur.execute(sql)
	for airport in traffic_airports['low_traffic']:
		sql = 'INSERT INTO domesticTraffic VALUES('
		sql += '\"' + airport + '\"' + ',' + str(0.8) + ');'
		cur.execute(sql)

	traffic_airports = get_traffic('HYD', international_airports, 100, 300)
	cur.execute('CREATE TABLE IF NOT EXISTS internationalTraffic(airport VARCHAR(255), weight DOUBLE);')
	for airport in traffic_airports['high_traffic']:
		sql = 'INSERT INTO internationalTraffic VALUES('
		sql += '\"' + airport + '\"' + ',' + str(0.9) + ');'
		cur.execute(sql)
	for airport in traffic_airports['medium_traffic']:
		sql = 'INSERT INTO internationalTraffic VALUES('
		sql += '\"' + airport + '\"' + ',' + str(0.85) + ');'
		cur.execute(sql)
	for airport in traffic_airports['low_traffic']:
		sql = 'INSERT INTO internationalTraffic VALUES('
		sql += '\"' + airport + '\"' + ',' + str(0.8) + ');'
		cur.execute(sql)

	con.commit()
	cur.close()

if __name__ == '__main__':
	populate_domestic_db()	



	

