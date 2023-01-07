import random

def keepDictUnder(theDict, underCount):
	if len(theDict.keys()) > underCount:
		for curUsername in theDict:
			if random.randint(1, 2) == 1:
				theDict.pop(curUsername, None)

def getVal(theDict, thePath):
	try:
		for i in range(len(thePath)):
			theDict = theDict[thePath[0]]
			thePath.pop(0)
		return theDict
	except:
		return None

def prettyTimeStr(theTime):
	curTime = time.time()

	timeDiff = abs(theTime - curTime)

	timeWord = ''

	if timeDiff < 1:
		return 'right now'
	elif timeDiff < 60:
		timeWord = 'second'
	elif timeDiff < 3600:
		timeWord = 'minute'
		timeDiff /= 60
	elif timeDiff < 86400:
		timeWord = 'hour'
		timeDiff /= 3600
	elif timeDiff < 2678400:
		timeWord = 'day'
		timeDiff /= 86400
	elif timeDiff < 31536000:
		timeWord = 'month'
		timeDiff /= 2678400

	timeDiff = math.floor(timeDiff)

	if timeDiff > 1:
		timeWord += 's'

	if theTime > curTime:
		return f'in {timeDiff} {timeWord}'
	else:
		return f'{timeDiff} {timeWord} ago'