import csv
def get_airports():
	f = open('airports.txt', 'rb')
	domestic_airports = ['HYD']
	international_airports = ['HYD']
	for line in f:
		data = line.split(',')
		if "India" in data[3]:
			if '\\N' not in data[4]:
				x = data[4][1:-1]
				if x not in domestic_airports:
					domestic_airports.append(x)
		else:
			if '\\N' not in data[4]:
				x = data[4][1:-1]
				if x not in international_airports:
					international_airports.append(x)


	return domestic_airports, international_airports

def get_IATAcode(place):
	idx = place.find('(') + 1
	place = place[idx:idx+3]
	if place == 'KJF':
		place = 'JFK'
	return place

def get_traffic(airport_name, airports, low_traffic_threshold, high_traffic_threshold):
	f = open('history2.csv', 'rb')
	traffic = {}

	for airport in airports:
		traffic[airport] = 0
	i = 0
	csv_reader = csv.reader(f)
	for row in csv_reader:
		if i == 0:
			i += 1
			continue
		row[2] = get_IATAcode(row[2])
		row[3] = get_IATAcode(row[3])
		if (row[2] in airports) and (row[3] in airports):
			if airport_name != row[2]:
				place = row[2]
			if airport_name != row[3]:
				place = row[3]
			traffic[place] += 1

	places = {'low_traffic' : [], 'medium_traffic' : [], 'high_traffic' : [airport_name]}

	for key, val in traffic.iteritems():
		if key == airport_name:
			continue
		if val >= high_traffic_threshold:
			places['high_traffic'].append(key)
		elif val < low_traffic_threshold:
			places['low_traffic'].append(key)
		else:
			places['medium_traffic'].append(key)

	if airport_name not in places['high_traffic']:
		places['high_traffic'].append(airport_name)
	return places		


domestic_airports, intl_airports = get_airports()
# print get_traffic('HYD', domestic_airports, 200, 400)
# print get_traffic('HYD', intl_airports, 200, 400)