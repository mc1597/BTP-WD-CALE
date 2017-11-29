import csv
import random
import MySQLdb as db
import datetime
from get_places import *
def get_time(arg):
	arg = arg[:7]
	if arg.find(':') == -1:
		return "null"
	if arg == '':
		arg = '00:00:00'
	else:
		if arg.find('M') != -1:	
			d = datetime.datetime.strptime(arg, '%I:%M%p')
		else:
			arg = arg[:5]
			d = datetime.datetime.strptime(arg, '%H:%M')
		arg = d.strftime('%T')
	return arg

def initialize_database(airport_name):
	place_to_gate_mapping = {'HYD' : '24', 'CCU' : '26', 'TIR' : '25A', 'BOM' : '22', 'VNS' : '23', 'MAA' : '26',
							 'LKO' : '28' , 'DEL' : '30A' , 'CJB' : '30B', 'VGA' : '25A', 'BLR' : '25B', 'IDR' : '25C',
							 'BBI' : '25D', 'VTZ' : '25E', 'RPR' : '25F', 'GAU' : '25G', 'PNQ' : '25H', 'RJA' : '26', 
							 'SIN' : '28' , 'IXM' : '30A' , 'DED' : '30B', 'IXE' : '25A', 'KUL' : '25B', 'AUH' : '25C',
							 'DXB' : '24', 'PAT' : '26', 'NAG' : '25A', 'PAB' : '22', 'AGX' : '23', 'AGR' : '26'
							}
	al = 'HYD'
	domestic_airports, intl_airports = get_airports()
	airports = domestic_airports + intl_airports
	con = db.connect(host = "localhost", user = "root", passwd = "password")
	cur = con.cursor()
	cur.execute('CREATE DATABASE IF NOT EXISTS HistoricFlightData;')
	cur.execute('USE HistoricFlightData;')
	f = open('history2.csv', 'rb')
	csv_reader = csv.reader(f)
	i = 0;
	sql = ""
	for row in csv_reader:
		unknown_flag = False
		airport_found = False	

		if i == 0:
			sql = 'CREATE TABLE IF NOT EXISTS flight_history (FlightDate DATE, Aircraft VARCHAR(255), Origin VARCHAR(255), Destination VARCHAR(255), FlightTime TIME, flight_no VARCHAR(255), airline VARCHAR(255), GateNumber VARCHAR(255), numP DOUBLE);'
		else:
			sql = 'INSERT INTO flight_history VALUES ('
			j = 0;
			for j in range(len(row)):
				airport_found = False	
				if (airport_name in row[2]) or (airport_name in row[3]):
					airport_found = True
				if airport_found == False:
					break		
				if j == 0:
					d = datetime.datetime.strptime(row[j],'%d-%b-%Y').date()
					arg = d.strftime('%Y-%m-%d')
					#print 'date',arg
					sql += '\"' + arg + '\"' + ','
				elif j == 1:
					sql += '\"' + row[j] + '\"' + ','
				elif j == 2:
					for airport in airports:
						if airport in row[j]:
							break
					sql += '\"' + airport + '\"' + ','
					if airport != airport_name:
						al = airport
				elif j == 3:
					for airport in airports:
						if airport in row[j]:
							break
					sql += '\"' + airport + '\"' + ','
					if airport != airport_name:
						al = airport
				elif j == 4:
					if airport != airport_name:
						arg = get_time(row[j])
						if arg == "null":
							unknown_flag = True
							break
						sql += "\"" + str(arg) + "\"" + ','
				elif j == 5:
					if airport == airport_name:
						arg = get_time(row[j])
						if arg == "null":
							unknown_flag = True
							break
						sql += "\"" + str(arg) + "\"" + ','
							
				elif j == 7:
					# al = row[j][:2]
					sql += '\"' + row[j] + '\"' + ','
					sql += '\"' + row[j][:2] + '\"' + ','

				

			if (unknown_flag == True) or (airport_found == False):
				i += 1
				continue
			try:
				sql += '\"' + place_to_gate_mapping[al] + '\"' + ','
				sql +=  '0);'
			except:	

				foo = ['24', '26', '22', '23', '26','28', '30A', '30B', '25A', '25B', '25C']
				gate = (random.choice(foo))
				sql += '\"' + gate + '\"' + ',' 
				sql +=  '0);'

		i = i + 1
		cur.execute(sql)

	con.commit()
	cur.close()	
if __name__ == '__main__':
	initialize_database('HYD')
