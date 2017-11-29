import csv
import time
import copy
import random
import datetime

gates = ['22','23','24','25A','25B','25C','26','28','30A','30B']	
dist = {'22' : 30,'23' : 28,'24' : 26,'26' : 18,'28' : 16,'30A' : 14,'30B' : 12,'25A' : 24 ,'25B' : 22 ,'25C' : 20}

def convert_time(time1):	
	[h, m, s] = [x for x in str(time1).split(':')]
	x = datetime.timedelta(hours = int(h), minutes = int(m), seconds = int(s))
	return x.seconds

def atoi(s):
    rtr=0
    for c in s:
        rtr=rtr*10 + ord(c) - ord('0')

    return rtr

def compareTimesLesser(time1, time2):
	t1 = datetime.datetime.strptime(time1,'%H:%M:%S')
	t2 = datetime.datetime.strptime(time2,'%H:%M:%S')
	if t1.time() <= t2.time():
		return True
	else:
		return False	

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

class node:

	def __init__(self, flight_no, actual_time, numPass):
		self.flight_no = flight_no
		self.actual_time = self.setTime(actual_time)		
		self.start_time = setStartTime(actual_time, 30)
		self.end_time = setEndTime(actual_time, 30)
		self.numPass = numPass

	def setTime(self, time):
		hr = time.split(':')[0]
		if len(hr) == 1:
			hr = '0' + hr
		return hr + ':' + time.split(':')[1] + ':' + time.split(':')[2]      

def populate(date):
	
	# candidate = {'22': {'flights' : [nodes], 'objVal' : 22}, '23' : {}}
	candidate = {}
	fname = 'dummydata2_'+date+'.csv'	
	with open(fname,'rb') as csvfile:
		data = csv.reader(csvfile)
		for row in data:
			if row[3].strip() not in candidate.keys():
				walkingDistance = dist[row[3].strip()]
				candidate[row[3].strip()] = {'flights':[],'objVal' : walkingDistance}
			candidate[row[3].strip()]['flights'].append(node(row[0].strip(),row[1].strip(),row[2].strip()))	

 	return candidate				

def greedyPopulate(date):
	
	# candidate = {'22': {'flights' : [nodes], 'objVal' : 22}, '23' : {}}
	candidate = {}
	fname = "greedy_" + date + ".txt"
	with open(fname,'rb') as csvfile:
		data = csv.reader(csvfile)
		for row in data:
			if row[3].strip() not in candidate.keys():
				walkingDistance = dist[row[3].strip()]
				candidate[row[3].strip()] = {'flights':[],'objVal' : walkingDistance}
			candidate[row[3].strip()]['flights'].append(node(row[0].strip(),row[1].strip(),row[2].strip()))	

 	return candidate				


def getNumOfFlights(date):
	fname = 'dummydata2_'+date+'.csv'
	with open(fname) as f:
		x = sum(1 for line in f)
	return x
    	
def conflict(tempMapping,flight,g):
	flight_start_time = time.strptime(flight.start_time, '%H:%M:%S')
	flight_end_time = time.strptime(flight.end_time, '%H:%M:%S')
	for f in tempMapping[g]['flights']:
		f_start_time = time.strptime(f.start_time, '%H:%M:%S')
		f_end_time = time.strptime(f.end_time, '%H:%M:%S')
		if not(convert_time(f.start_time) > convert_time(flight.end_time) or convert_time(flight.start_time) > convert_time(f.end_time)):
			return True
	return False

def sortMapping(candidate):
	tempMapping = copy.deepcopy(candidate)
	for gate in tempMapping:
		tempList = tempMapping[gate]['flights']
		tempList.sort(key=lambda x: x.actual_time)
		tempMapping[gate]['flights'] = tempList
	return tempMapping 

def swap(candidate):
	neighbourhood = []
	tempMapping = copy.deepcopy(candidate)	
	interval_start = '0'
	interval_end = '0'
	sortedMapping = sortMapping(tempMapping)
	for gate_index1 in range(len(gates)):
		gate = gates[gate_index1]		
		for i in range(len(sortedMapping[gate]['flights'])-1):
			flight1 = sortedMapping[gate]['flights'][i]			
			
			for gate_index2 in range(gate_index1 + 1,len(gates)):
				g = gates[gate_index2]
				
				for j in range(len(sortedMapping[g]['flights'])-1):
					f1 = sortedMapping[g]['flights'][j]
				
				
				if compareTimesLesser(flight1.start_time,f1.start_time):
					interval_start = flight1.start_time
				else:
					interval_start = f1.start_time
				if compareTimesLesser(f1.end_time,flight1.end_time):
					interval_end = flight1.end_time
				else:
					interval_end = f1.end_time

				flag1 = False	
				flag2 = False	
				for testFlight1 in tempMapping[gate]['flights']:
					if compareTimesLesser(interval_start, testFlight1.start_time) and compareTimesLesser(testFlight1.end_time, interval_end):
						if testFlight1.flight_no == flight1.flight_no and testFlight1.actual_time == flight1.actual_time:
								continue
						else:
							flag1 = True
							break		
				if flag1 == False:
					for testFlight2 in tempMapping[g]['flights']:
						if compareTimesLesser(interval_start, testFlight2.start_time) and compareTimesLesser(testFlight2.end_time, interval_end):
							if testFlight2.flight_no == f1.flight_no and testFlight2.actual_time == f1.actual_time:
									continue
							else:									
								flag2 = True
								break	
				if flag1 == False and flag2 == False:
					tempList = []
					for ft in tempMapping[gate]['flights']:
						if ft.flight_no != flight1.flight_no and ft.actual_time != flight1.actual_time:
							tempList.append(ft)			
					tempMapping[gate]['flights'] = tempList				
					tempMapping[gate]['flights'].append(f1)					

					tempList = []
					for ft in tempMapping[g]['flights']:
						if ft.flight_no != f1.flight_no and ft.actual_time != f1.actual_time:
							tempList.append(ft)			
					tempMapping[g]['flights'] = tempList				
					tempMapping[g]['flights'].append(flight1)		
					neighbourhood.append(tempMapping)
					tempMapping = copy.deepcopy(candidate)

	return neighbourhood
	
def getIntervalExchangeNeighbourhood(candidate):	 
	neighbourhood = []
	tempMapping = copy.deepcopy(candidate)
	interval1_start = '0'
	interval1_end = '0'
	interval_start = '0'
	interval_end = '0'
	sortedMapping = sortMapping(tempMapping)
	for gate_index1 in range(len(gates)):
		gate = gates[gate_index1]		
		for i in range(len(sortedMapping[gate]['flights'])-1):
			flight1 = sortedMapping[gate]['flights'][i]
			flight2 = sortedMapping[gate]['flights'][i+1]
			if compareTimesLesser(flight1.start_time, flight2.start_time):
				interval1_start = flight1.start_time
			else:
				interval1_start = flight2.start_time	
			if compareTimesLesser(flight2.end_time, flight1.end_time):
				interval1_end = flight1.end_time
			else:
				interval1_end = flight2.end_time
			for gate_index2 in range(gate_index1 + 1,len(gates)):
				g = gates[gate_index2]
				interval2_start = '0'
				interval2_end = '0'			
				for j in range(len(sortedMapping[g]['flights'])-1):
					f1 = sortedMapping[g]['flights'][j]
					f2 = sortedMapping[g]['flights'][j+1]
					if compareTimesLesser(f1.start_time, f2.start_time):
						interval2_start = f1.start_time
					else:
						interval2_start = f2.start_time	
					if compareTimesLesser(f2.end_time, f1.end_time):
						interval2_end = f1.end_time
					else:
						interval2_end = f2.end_time

				if compareTimesLesser(interval1_start, interval2_start):
					interval_start = interval1_start
				else:
					interval_start = interval2_start
				if compareTimesLesser(interval2_end, interval1_end):
					interval_end = interval1_end
				else:
					interval_end = interval2_end

				flag1 = False	
				flag2 = False	
				for testFlight1 in tempMapping[gate]['flights']:
					if compareTimesLesser(interval_start, testFlight1.start_time) and compareTimesLesser(testFlight1.end_time, interval_end):
						if (testFlight1.flight_no == flight1.flight_no and testFlight1.actual_time == flight1.actual_time) or (testFlight1.flight_no == flight2.flight_no and testFlight1.actual_time == flight2.actual_time):
								continue
						else:
							flag1 = True
							break		
				if flag1 == False:
					for testFlight2 in tempMapping[g]['flights']:
						if compareTimesLesser(interval_start, testFlight2.start_time) and compareTimesLesser(testFlight2.end_time, interval_end):
							if (testFlight2.flight_no == f1.flight_no and testFlight2.actual_time == f1.actual_time) or (testFlight2.flight_no == f2.flight_no and testFlight2.actual_time == f2.actual_time):
									continue
							else:								
								flag2 = True
								break		
				
				if flag1 == False and flag2 == False:				
					tempList = []
					for ft in tempMapping[gate]['flights']:
						if (ft.flight_no != flight1.flight_no and ft.actual_time != flight1.actual_time) and (ft.flight_no != flight2.flight_no and ft.actual_time != flight2.actual_time):
							tempList.append(ft)			
					tempMapping[gate]['flights'] = tempList				
					tempMapping[gate]['flights'].append(f1)
					tempMapping[gate]['flights'].append(f2)

					tempList = []
					for ft in tempMapping[g]['flights']:
						if (ft.flight_no != f1.flight_no and ft.actual_time != f1.actual_time) and (ft.flight_no != f2.flight_no and ft.actual_time != f2.actual_time):
							tempList.append(ft)			
					tempMapping[g]['flights'] = tempList				
					tempMapping[g]['flights'].append(flight1)
					tempMapping[g]['flights'].append(flight2)
					neighbourhood.append(tempMapping)
					tempMapping = copy.deepcopy(candidate)

	
	return neighbourhood
					
def getInsertMoveNeighbourhood(candidate):	 
	# bestNeighbour = copy.deepcopy(candidate)
	# bestVal = calcObj(candidate)
	neighbourhood = []
	tempMapping = copy.deepcopy(candidate)
	for gate in gates:
		for flight in tempMapping[gate]['flights']:			
			for g in gates:				
				if g != gate:
					if conflict(tempMapping,flight,g) == False:
						#  Uncomment later
						# print "flight",flight.flight_no, flight.actual_time,"remove from:", gate, "add to:", g
						# print "Mapping: "
						# for gate1 in tempMapping.values():
						# 	print "gateNo", gate1['objVal']		
						# 	for flight1 in gate1['flights']:
						# 		print flight1.flight_no,flight1.actual_time, gate1['objVal']

						tempList = []
						for flight2 in tempMapping[gate]['flights']:
							if flight2.flight_no != flight.flight_no and flight2.actual_time != flight.actual_time:
								tempList.append(flight2)

						
						tempMapping[gate]['flights'] = tempList
						tempMapping[g]['flights'].append(flight)								
						
						# currVal = calcObj(tempMapping)
						# if currVal <  bestVal:
						# 	bestNeighbour = copy.deepcopy(tempMapping)
						# 	bestVal = currVal
						neighbourhood.append(tempMapping)
						tempMapping = copy.deepcopy(candidate)

	return neighbourhood

def totalPass(tempMapping, gate):
	val = 0
	for f in gate['flights']:
		val += int(f.numPass)
	return val	

def calcObj(tempMapping, date):
	val = 0
	for gate in tempMapping.values():
		val += gate['objVal']*totalPass(tempMapping,gate) 
	return float(val)

def printMapping(candidate):
	for k, v in candidate.iteritems():
		print k
		for flight in v['flights']:
			print flight.flight_no,flight.actual_time,flight.numPass
		
if __name__ == '__main__':
	date = sys.argv[1]
	candidate = populate(date)
	# printMapping(candidate)