import requests
import time
import random

import config
import util

playerQueue = []
playerLastSeens = {}

def getQueuedPlayer():
	global playerQueue

	if len(playerQueue) > 0:
		curQueued = random.choice(playerQueue)
		playerQueue.remove(curQueued)
		return curQueued
	else:
		getNewPlayers()
		return getQueuedPlayer() # epic recursion

def getNewPlayers():
	curTime = time.time()

	usernamesApiUrl = f'https://pit-grinder-logic-api-jlrw3.ondigitalocean.app/api/{config.usernamesApiKey}/recentplayers'
	usernamesApiGot = requests.get(usernamesApiUrl, timeout = 5).json()

	for curUsername in usernamesApiGot.get('usernames', []):
		setPlayerLastSeen(curUsername, curTime)

def setPlayerLastSeen(playerUsername, toTime):
	global playerLastSeens

	curTime = time.time()

	if playerUsername not in playerLastSeens:
		playerQueue.append(playerUsername)

	if curTime - playerLastSeens.get(playerUsername, curTime) > 120:
		playerQueue.append(playerUsername)

	playerLastSeens[playerUsername] = toTime

	util.keepDictUnder(playerLastSeens, 8192)