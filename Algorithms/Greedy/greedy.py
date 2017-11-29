import csv
import MySQLdb as db
import sys
from flightNode import *
import operator
from preprocess_greedy import *

mapping = {'22' : [], '23' : [], '24' : [], '26' : [], '28': [], '30A' : [], '30B' : [], '25A' : [], '25B' : [], '25C' : []}
gates = ['30B','30A','28','26','25C','25B','25A','24','23','22']
dist = {'22' : 30,'23' : 28,'24' : 26,'26' : 18,'28' : 16,'30A' : 14,'30B' : 12,'25A' : 24 ,'25B' : 22 ,'25C' : 20}

def convert_time(time):
	[h, m, s] = [x for x in time.split(':')]
	x = datetime.timedelta(hours = int(h), minutes = int(m), seconds = int(s))
	return x.seconds

def conflictP(gate,flightTime):	
	flight_start_time = setStartTime(flightTime,30)
	flight_end_time = setEndTime(flightTime,30)
	for f in mapping[gate]:
		f_start_time = setStartTime(f[1],30)
		f_end_time = setEndTime(f[1],30)
		if not(convert_time(f_start_time) > convert_time(flight_end_time) or convert_time(flight_start_time) > convert_time(f_end_time)):
			return True
	return False

def greedyAlgo():
	fname2 = 'dummydata1.csv'		
	filer = csv.reader(open(fname2), delimiter=",")
	# sortedlist = sorted(filer, key=operator.itemgetter(2), reverse=True)
	sortedlist = sorted(filer, key=lambda row: int(row[2]), reverse=True)	
	tot = len(gates)
	for flight in sortedlist:
		# print flight
		i = 0
		ctr = 0
		while conflictP(gates[i],flight[1]):
				i = (i + 1) % tot
				ctr += 1
				if ctr >= tot:
					break
		if conflictP(gates[i], flight[1]) == False:
			mapping[gates[i]].append(flight)
	
	return mapping		


def totalPass(tempMapping, gate):
	val = 0
	for f in tempMapping[gate]:
		val += float(f[2])
	return val	

def calcObj1(tempMapping):
	val = 0
	for gate in gates:
		val += dist[gate]*totalPass(tempMapping,gate) 
	return float(val)

if __name__ == '__main__':

	date = sys.argv[1]
	preprocessG(date)
	mapping = greedyAlgo()	
	fname = 'greedy_' + date +'.txt'
	file = open(fname, 'wb')
	for gate in gates:
		

		for flight in mapping[gate]:
			# file.write(flight)
			for item in flight:
  				file.write("%s," % item)
  			file.write(gate)	
  			file.write("\n")	

	print calcObj1(mapping)

