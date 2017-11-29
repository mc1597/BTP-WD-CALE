import random
import datetime
import sys
import copy
import pickle
from collections import defaultdict

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

def get_greedy_population(date):
	gates = ['22','23','24','26','28','30A','30B','25A','25B','25C']
	mapping = {'22' : [], '23' : [], '24' : [], '26' : [], '28': [], '30A' : [], '30B' : [], '25A' : [], '25B' : [], '25C' : []}
	f = open("greedy_" + date + ".txt", 'rb')
	flights = []
	initial_population = []
	for l in f.readlines():
		l = l.strip("\n")
		r = l.split(",");
		f = flight(str(r[1]), r[3], int(r[2]), 0)
		flights.append(f)

	flights.sort(key=lambda x:convert_time(x.dept_time))
	cnt = 0
	for f in flights:
		f.id = cnt
		cnt += 1
	c = candidate(flights)
	initial_population.append(c)
	initial_population.append(c)

	return initial_population

def get_initial_population(population_size , date):
	filename = 'dummydata2_' + date + '.txt'
	# f = open(filename, 'rb')	
	# initial_population = f.read()
	with open (filename, 'rb') as fp:
		initial_population = pickle.load(fp)	
	return initial_population

def can_swap(candidate1, candidate2, flight1, flight2):
	is_conflict2 = False
	for f1 in candidate1.flights:
		if f1.gate == flight2.gate:
			if not(convert_time(f1.start_time) > convert_time(flight2.end_time) or convert_time(flight2.start_time) > convert_time(f1.end_time)):
				is_conflict2 = True
				break
	is_conflict1 = False
	for f2 in candidate2.flights:
		if f2.gate == flight1.gate:
			if not(convert_time(f2.start_time) > convert_time(flight1.end_time) or convert_time(flight1.start_time) > convert_time(f2.end_time)):
				is_conflict1 = True
				break
	if is_conflict1 == False and is_conflict2 == False:
		return True
	return False		

def onepoint_crossover(candidate1, candidate2):
	cross_point = random.randint(len(candidate1.flights)/4, 3 * len(candidate1.flights)/4)

	for i in range(0, cross_point):
		f1 = candidate1.flights[i]
		f2 = candidate2.flights[i]
		if can_swap(candidate1, candidate2, f1, f2):
			candidate1.flights[i].gate = f2.gate
			candidate2.flights[i].gate = f1.gate

	return candidate1, candidate2

def uniform_crossover(candidate1, candidate2):
	for i in range(0, len(candidate1.flights)):
		f1 = candidate1.flights[i]
		f2 = candidate2.flights[i]
		r = random.randint(0, 1)
		if r == 1:
			if can_swap(candidate1, candidate2, f1, f2):
				candidate1.flights[i].gate = f2.gate
				candidate2.flights[i].gate = f1.gate

	return candidate1, candidate2

def multipoint_crossover(candidate1, candidate2):
	cross_point1 = random.randint(0, len(candidate1.flights)/2)
	cross_point2 = random.randint(len(candidate1.flights)/2, len(candidate1.flights))

	for i in range(0, cross_point1):
		f1 = candidate1.flights[i]
		f2 = candidate2.flights[i]
		if can_swap(candidate1, candidate2, f1, f2):
			candidate1.flights[i].gate = f2.gate
			candidate2.flights[i].gate = f1.gate

	for i in range(cross_point2, len(candidate1.flights)):
		f1 = candidate1.flights[i]
		f2 = candidate2.flights[i]
		if can_swap(candidate1, candidate2, f1, f2):
			candidate1.flights[i].gate = f2.gate
			candidate2.flights[i].gate = f1.gate

	return candidate1, candidate2


def generative_main(date, noi, initial_population, n):
		
	parent_population = initial_population

	iter_no = 0
	while iter_no < noi:
		# print "Parent fitness 1"
		# for p in parent_population:
		# 	print p.get_fitness(),
		# print " "	
		children_population = []
		for i in range(len(parent_population)/2):
			c1 = copy.deepcopy(parent_population[i])
			for j in range(len(parent_population)/2 , len(parent_population)):
				c2 = copy.deepcopy(parent_population[j])			
				child1, child2 = uniform_crossover(c1, c2)
				children_population.append(child1)
				children_population.append(child2)
		
		children_population.sort(key=lambda x:x.get_fitness())		
		children_population = children_population[:n]

		# print "Crossover fitness"
		# for p in children_population:
		# 	print p.get_fitness(),
		# print " "

		# print "Parent fitness 2"
		# for p in parent_population:
		# 	print p.get_fitness(),
		# print " "	

		for i in range(len(children_population)):
			child = copy.deepcopy(children_population[i])
			child.insert_mutate()
			children_population[i] = child

		# print "Mutation fitness"
		# for p in children_population:
		# 	print p.get_fitness(),
		# print " "
	
		# print "Parent fitness 3"
		# for p in parent_population:
		# 	print p.get_fitness(),
		# print " "	

		total_population = parent_population + children_population
		total_population.sort(key=lambda x:x.get_fitness())			
		parent_population = total_population[:n]

		# print "Final fitness"
		
		# print "Iteration:",iter_no
		# for p in parent_population:
		# 	print p.get_fitness(),
		# print " "	
		iter_no += 1
		

	return parent_population[0].get_fitness()

def steady_main(date, noi, initial_population, n):

	parent_population = initial_population
	best_fitness_per_iteration = []

	iter_no = 0
	flag = 0
	while iter_no < noi:
		# print "iter no", iter_no
		# print "len of parent", len(parent_population)	
		children_population = []
		for i in range(len(parent_population)/2):
			# print "i", i
			c1 = copy.deepcopy(parent_population[i])
			for j in range(len(parent_population)/2 , len(parent_population)):
				# print "j", j
				c2 = copy.deepcopy(parent_population[j])		
				# print len(c1.flights),len(c2.flights)	
				child1, child2 = uniform_crossover(c1, c2)
				children_population.append(child1)
				children_population.append(child2)
		
		children_population.sort(key=lambda x:x.get_fitness())
		if flag == 1:		
			children_population = children_population[:n]

		# print "flag", flag
		# print "len of children", len(children_population)
		for i in range(len(children_population)):
			child = copy.deepcopy(children_population[i])
			child.insert_mutate()
			children_population[i] = child
			# print "child",len(child.flights)
		total_population = parent_population + children_population
		total_population.sort(key=lambda x:x.get_fitness())
		if flag == 1:
			iter_no += 1			
			parent_population = total_population[:n]
			# iter_no += 1	
		else:
			parent_population = total_population

		# for p in parent_population:
		# 	print p.get_fitness(),
		# print "\n"

		if len(parent_population) >= n:
			flag = 1
			parent_population = parent_population[:n]
		if flag == 1:
			best_fitness_per_iteration.append(parent_population[0].get_fitness())
		# print "Final fitness"
		
		# print "Iteration:",iter_no
		# for p in parent_population:
		# 	print p.get_fitness(),
		# print " "					
	return best_fitness_per_iteration	

def genetic_main(n, maxIterations, dateList, is_generative):
	fitnessList = {}
	iter_no = 0
	avgVal = 0
	objVal = []
	objValAll = []
	for date in dateList:
		fitnessList[date] = []

	#is_generative = 0	#comment this later

	for date in dateList:
		if is_generative:	
			# init2 = get_greedy_population(date)
			# initial_population = init2 + get_initial_population(n-2, date)			
			initial_population = get_initial_population(n, date) #Steady + RR
		else:			
			# initial_population = get_initial_population(n, date)
			initial_population = get_greedy_population(date) #Steady + Greedy

		# iter_no = 0
		# while iter_no < maxIterations:	
		# 	if is_generative:
		# 		fitnessList[date].append(generative_main(date,iter_no+1,initial_population,n))
		# 	else:
		# 		fitnessList[date].append(steady_main(date,iter_no+1,initial_population,n))
		# 	iter_no += 1

		fitnessList[date].append(steady_main(date,maxIterations,initial_population,n))		
		#objVal.append(fitnessList[date][-1])		
		objValAll.append(fitnessList[date][0])

	print "ObjValAll",objValAll	
	# iter_no = 0	
	# sumFV = 0	
	# for i in range(len(dateList)):
	# 	sumFV += float(objVal[i])
	# avgVal = sumFV/float(len(dateList))

	# sumVar = 0
	# for i in range(len(dateList)):
	# 	sumVar += (objVal[i] - avgVal) * (objVal[i] - avgVal)
	# var = float(sumVar) / float(len(dateList))
	
	avgObjValALL = [0 for i in range(maxIterations)]
	for dt in range(len(dateList)):
		for iterno in range(maxIterations):
			avgObjValALL[iterno] += objValAll[dt][iterno]

	avgObjValALL = [i/float(len(dateList)) for i in avgObjValALL]
	print "Objective val in every iter",avgObjValALL		
	# return var, avgVal, objVal	
	

if __name__ == '__main__':
	maxIterations = int(sys.argv[1])
	population_size = int(sys.argv[2])
	is_generative = int(sys.argv[3])
	#dateList = ['2017-01-09','2017-01-08','2017-01-07','2017-01-06','2017-01-05','2017-01-04','2017-01-03']
	print "############################"
	dateList = []
	for i in range(4, len(sys.argv)):
		dateList.append(sys.argv[i])	
	genetic_main(population_size, maxIterations, dateList, is_generative)
	
	print "Population Size:", population_size
	print "Num of Iterations:", maxIterations
	# print "avgVals:",avgVals	
	# print "objVal:",objVal
	# print "Variance:",var
	print "############################"