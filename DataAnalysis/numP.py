import MySQLdb as db

if __name__ == '__main__':
	con = db.connect(host = "localhost", user = "root", passwd = "password")
	cur = con.cursor()
	cur.execute('USE HistoricFlightData;')
	sql = 'SELECT * FROM flight_history;'

	cur.execute(sql);
	result = cur.fetchall()
	for record in result:
		print record
