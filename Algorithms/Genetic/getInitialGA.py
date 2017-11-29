import random
import datetime
import MySQLdb as db
import sys
import copy
import pickle

mutate_counter = 10
gates = ['30B','30A','28','26','25C','25B','25A','24','23','22']
distance = {'22' : 30,'23' : 28,'24' : 26,'26' : 18,'28' : 16,'30A' : 14,'30B' : 12,'25A' : 24 ,'25B' : 22 ,'25C' : 20}

def atoi(s):
    rtr=0
    for c in s:
        rtr=rtr*10 + ord(c) - ord('0')

    return rtr

def convert_time(time):
	[h, m, s] = [x for x in time.split(':')]
	x = datetime.timedelta(hours = int(h), minutes = int(m), seconds = int(s))
	return x.seconds

def setStartTime(actual_time, buffer_time):
	hr = actual_time.split(':')[0]
	mn = actual_time.split(':')[1]
	if len(mn) == 1:
		mn = '0' + mn
	if len(hr) == 1:
		hr = '0' + hr    
	if atoi(mn) < buffer_time and hr!='00':
		hr = str(atoi(hr) - 1)        
		mn = str(atoi(mn) + 60 - buffer_time)        
	elif atoi(mn) < buffer_time:
		hr = '23'
		mn = str(atoi(mn) + 60 - buffer_time)
	else:
		mn = str(atoi(mn) - buffer_time)
	if len(mn) == 1:
		mn = '0' + mn
	if len(hr) == 1:
		hr = '0' + hr
	return hr + ':' + mn + ':' + actual_time.split(':')[2]  

def setEndTime(actual_time, delay):
	boundary = 60 - delay
	hr = actual_time.split(':')[0]
	mn = actual_time.split(':')[1]
	if len(mn) == 1:
		mn = '0' + mn
	if len(hr) == 1:
		hr = '0' + hr    
	if atoi(mn) >= boundary and hr!='23':
		hr = str(atoi(hr) + 1)        
		mn = str(atoi(mn) - boundary)        
	elif atoi(mn) > boundary:
		hr = '00'
		mn = str(atoi(mn) - boundary)
	else:
		mn = str(atoi(mn) + delay)
	if len(mn) == 1:
		mn = '0' + mn
	if len(hr) == 1:
		hr = '0' + hr    
	return hr + ':' + mn + ':' + actual_time.split(':')[2]      

class flight:
	def __init__(self, dept_time, gate, population, flight_id):
		self.dept_time = dept_time
		self.start_time = setStartTime(dept_time, 30)
		self.end_time = setEndTime(dept_time, 30)
		self.gate = gate
		self.population = population
		self.id = flight_id

def conflictP(mapping, gate, cur_flight):
	for f in mapping[gate]:
		if not(convert_time(f.start_time) > convert_time(cur_flight.end_time) or convert_time(cur_flight.start_time) > convert_time(f.end_time)):
			return True
	return False

class candidate:
	def __init__(self, flights):
		self.flights = flights

	def get_fitness(self):
		fitness = 0
		for f in self.flights:

			# print "fitness:",f.gate, f.population,f.id
			fitness += distance[f.gate] * f.population
		return fitness


	def insert_mutate(self):
		# print "len of flights",len(self.flights)
		if len(self.flights) != 0:

			index = random.randint(0, len(self.flights)-1)
			cur_flight = self.flights[index]
			count = 0
			g = cur_flight.gate
			while count < mutate_counter:
				count += 1
				g = gates[random.randint(0, len(gates)-1)]
				while True:
					if g == cur_flight.gate:
						g = gates[random.randint(0, len(gates)-1)]
					else:
						break
				is_conflict = False
				for f in self.flights:
					if f.gate == g:
						if not (convert_time(f.start_time) > convert_time(cur_flight.end_time) or convert_time(cur_flight.start_time) > convert_time(f.end_time)):
							is_conflict = True
							break
				if not is_conflict:
					break
			self.flights[index].gate = g

	def swap_mutate(self):
		count = 0
		is_conflict = False
		index1 = 0
		index2 = 0
		g1 = 0
		g2 = 0
		while count < mutate_counter:
			index1 = random.randint(0, len(self.flights)-1)
			index2 = random.randint(0, len(self.flights)-1)
			cur_flight1 = self.flights[index1]
			cur_flight2 = self.flights[index2]
			g1 = cur_flight1.gate
			g2 = cur_flight2.gate
			count += 1
			is_conflict = False
			for f in self.flights:
				if f.gate == g1:
					if not (convert_time(f.start_time) > convert_time(cur_flight1.end_time) or convert_time(cur_flight1.start_time) > convert_time(f.end_time)):
						is_conflict = True
						break
				if f.gate == g2:
					if not (convert_time(f.start_time) > convert_time(cur_flight2.end_time) or convert_time(cur_flight2.start_time) > convert_time(f.end_time)):
						is_conflict = True
						break
			if not is_conflict:
				break
		if not is_conflict:
			self.flights[index1].gate = g2
			self.flights[index2].gate = g1

def get_initial_population(population_size , date):
	gates = ['22','23','24','26','28','30A','30B','25A','25B','25C']
	mapping = {'22' : [], '23' : [], '24' : [], '26' : [], '28': [], '30A' : [], '30B' : [], '25A' : [], '25B' : [], '25C' : []}	
	con = db.connect(host = "localhost", user = "root", passwd = "password")
	cur = con.cursor()
	cur.execute('USE HistoricFlightData;')
	
	sql = 'SELECT flight_no,FlightTime,numP FROM passengerCount where FlightDate = \"' + date + '\" AND Origin = \"'+ "HYD" + '\"' + 'GROUP BY FlightTime;'		
	cur.execute(sql);
	records = cur.fetchall()
	initial_population = []
	for count in range(population_size):
		for gate in mapping:
			mapping[gate] = []
		index = random.randint(0, len(gates)-1)
		currGate = gates[index]
		ctr = 0
		for r in records:
			ct = 0
			
			f = flight(str(r[1]), gates[0], r[2], r[0])
			while conflictP(mapping, currGate, f):
				index = (index + 1) % len(gates)
				currGate = gates[index]
				ct += 1
				if ct > len(gates):
					break
			if ct >  len(gates):
				continue

			f.gate = currGate	
			mapping[currGate].append(f)
			index = random.randint(0, len(gates)-1)
		flights = []
		for gate in mapping:
			for f in mapping[gate]:
				flights.append(f)
		flights.sort(key=lambda x:convert_time(x.dept_time))
		cnt = 0
		for f in flights:
			f.id = cnt
			cnt += 1
		c = candidate(flights)
		initial_population.append(c)
	return initial_population

def main():

	date = sys.argv[1]

	initialPop = get_initial_population(5,date)
	filename = 'dummydata2_' + date + '.txt'
	# f = open(filename, 'wb')
	# f.write(initialPop)
	with open(filename, 'wb') as fp:
		pickle.dump(initialPop, fp)
	fp.close()

if __name__ == '__main__':
		main()	
