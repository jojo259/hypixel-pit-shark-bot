import os

import dotenv
dotenv.load_dotenv()

debugMode = False

if 'debugmode' in os.environ:
	debugMode = True
	print('running in DEBUG mode')
else:
	print('running in PRODUCTION mode')

discordWebhookUrl = os.environ['discordwebhookurl']
hypixelApiKey = os.environ['hypixelapikey']
usernamesApiKey = os.environ['usernamesapikey']