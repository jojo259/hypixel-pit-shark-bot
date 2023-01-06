import time
import random

import discordsender
import config
import indexer
import playermanager

discordsender.sendDiscord(f'`starting in {"debug" if config.debugMode else "production"} mode`', config.discordWebhookUrl)

indexedTimes = []

while True:
	try:
		curTime = time.time()
		if len(indexedTimes) < 120:
			indexedTimes.append(curTime)
			playerToCheck = playermanager.getQueuedPlayer()
			print(f'checking {playerToCheck}, checked {len(indexedTimes)} in last minute')
			indexer.indexPlayer(playerToCheck)
		else:
			time.sleep(1)
		indexedTimes = list(filter(lambda x: (x > curTime - 60), indexedTimes)) 
	except Exception as e:
		discordsender.sendDiscord(f'error: {e}', config.discordWebhookUrl)