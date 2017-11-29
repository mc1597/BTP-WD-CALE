from flightNode import *
import sys
from preprocess import *
from collections import defaultdict

def tabuSearch(noi, option, date):
	tabuList = []
	plotDict = {}
	# sbest = greedyPopulate(date)
	sbest = populate(date)
	tabuList.append([sbest, 0])
	iter_no = 1
	bestCandidate = sbest
	sNeighbourhood = []
	while(iter_no < noi):
		if option == 1:
			sNeighbourhood = getInsertMoveNeighbourhood(bestCandidate)
		if option == 2:
			sNeighbourhood = swap(bestCandidate)
		if option == 3:		
			sNeighbourhood = getIntervalExchangeNeighbourhood(bestCandidate)
		if option == 4:
			sNeighbourhood = getInsertMoveNeighbourhood(bestCandidate) + swap(bestCandidate)
		if option == 5:		
			sNeighbourhood = getInsertMoveNeighbourhood(bestCandidate) + getIntervalExchangeNeighbourhood(bestCandidate)
		if option == 6:		
			sNeighbourhood = swap(bestCandidate) + getIntervalExchangeNeighbourhood(bestCandidate)
			
		flag = False
		for sCandidate in sNeighbourhood:
			if sCandidate not in [i[0] for i in tabuList]:
				flag = True
				if calcObj(sCandidate, date) < calcObj(bestCandidate, date):
					bestCandidate = sCandidate

		earliestNeighbour = [bestCandidate, iter_no]
		if flag == False:
			for item in tabuList:
				if item[0] in sNeighbourhood:
					if earliestNeighbour[1] > item[1]:
						earliestNeighbour = item
			tabuList.remove(earliestNeighbour)
			bestCandidate = earliestNeighbour[0]

		if calcObj(bestCandidate, date) < calcObj(sbest, date):
			sbest = bestCandidate

		plotDict[iter_no] = calcObj(sbest, date)	
 		tabuList.append([bestCandidate, iter_no])
 		# print "Iteration:",iter_no,"Date:",date  		 		
 		# print "Obj Val of best candidate at this iter:"
 		# print calcObj(sbest, date)
		iter_no = iter_no + 1
	return sbest, plotDict

if __name__ == '__main__':
	date = sys.argv[1]
	preprocess(date)
	best,pd = tabuSearch(20, 5, date)
	printMapping(best)	
	print calcObj(best, date)