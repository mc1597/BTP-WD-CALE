import MySQLdb as db
import sys

def getColor(num):
	
	if num > 800.0:
		return 'r'
	elif num > 400.0:
		return 'y'
	else:
		return 'g'	

if __name__ == '__main__':
	
	con = db.connect(host = "localhost", user = "root", passwd = "password")
	cur = con.cursor()
	cur.execute('USE HistoricFlightData;')
	date = sys.argv[1]
	hour = sys.argv[2]
	gNum = sys.argv[3]
	airport_name = "HYD"
	sql = 'SELECT SUM(numP) FROM passengerCount where FlightDate = \"' + date + '\" AND FlightTime LIKE \"' + hour +':%%:%%\" AND gateNumber = \"'+ gNum + '\";'

	
	cur.execute(sql);
	result = cur.fetchone()
	try:
		col = str(getColor(float(result[0])))
	except:
		col = str(getColor(float('0')))

	sys.stdout.write(col)
