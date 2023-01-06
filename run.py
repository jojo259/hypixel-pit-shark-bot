import time

import discordsender
import config
import indexer
import playermanager

discordsender.sendDiscord(f'`starting in {"debug" if config.debugMode else "production"} mode`', config.discordWebhookUrl)

while True:
	try:
		playerToCheck = playermanager.getQueuedPlayer()
		print(f'checking {playerToCheck}')
		indexer.indexPlayer(playerToCheck)
		time.sleep(0.5)
	except Exception as e:
		discordsender.sendDiscord(f'error: {e}', config.discordWebhookUrl)