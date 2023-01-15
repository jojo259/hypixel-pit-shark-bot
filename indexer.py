import requests
import time
import io
import urllib
import json
import datetime

import nbt
from nbt.nbt import NBTFile, TAG_Long, TAG_Int, TAG_String, TAG_List, TAG_Compound

import config
import discordsender
import util
import checksharkable

alreadySentNonces = {}

def getHypixelApi(urlToGet):
	try:
		apiGot = requests.get(urlToGet, timeout = 10).json()
		if apiGot.get('success') == True:
			return apiGot
	except Exception as e:
		print(f'getHypixelApi {e}')
	return {'success': False}

def indexPlayer(playerUuid):
	if len(playerUuid) == 32:
		apiUrl = f'https://api.hypixel.net/player?key={config.hypixelApiKey}&uuid={playerUuid}'
	else:
		apiUrl = f'https://api.hypixel.net/player?key={config.hypixelApiKey}&name={playerUuid}'

	apiTimer = time.time()

	apiGot = getHypixelApi(apiUrl)
	if apiGot.get('success') != True:
		print(f'hypixel api failed')
		return

	playerXp = util.getVal(apiGot, ['player', 'stats', 'Pit', 'profile', 'xp'])

	if playerXp != None:
		if playerXp >= 610140:
			return

	playerItems = getItems(apiGot)
	for curItem in playerItems:

		itemNonce = util.getVal(curItem, ['tag','ExtraAttributes','Nonce'])

		if itemNonce in alreadySentNonces:
			continue

		matchedFilters = checksharkable.getItemMatchedSharkableFilters(curItem)

		if len(matchedFilters) == 0:
			continue

		itemCurLore = curItem.get('tag', {}).get('display', {}).get('Lore', [])
		itemCurLore.insert(0, f'Owner: {playerUuid}') # change to actual player username from api
		curItem['tag']['display']['Lore'] = itemCurLore

		print(f'sending item with nonce {itemNonce} with matched filters {matchedFilters}')
		alreadySentNonces[itemNonce] = True
		util.keepDictUnder(alreadySentNonces, 8192)
		itemImageUrl = 'https://www.jojo.boats/api/itemimage?itemjson=' + urllib.parse.quote_plus(json.dumps(curItem))
		messageEmbeds = [{
			'type': 'rich',
			'title': f'Matched filters: `{", ".join(matchedFilters)}`',
			'description': '',
			'color': 255,
			'image': {
				'url': itemImageUrl,
				'width': 0,
				'height': 0
			},
			'timestamp': str(datetime.datetime.now())
		}]
		discordsender.sendDiscord('Mystic found:', config.discordWebhookUrl, messageEmbeds)

def getItems(playerData):
	try:
		def unpack_nbt(tag): #credit CrypticPlasma on hypixel forums
			"""
			Unpack an NBT tag into a native Python data structure.
			"""

			if isinstance(tag, TAG_List):
				return [unpack_nbt(i) for i in tag.tags]
			elif isinstance(tag, TAG_Compound):
				return dict((i.name, unpack_nbt(i)) for i in tag.tags)
			else:
				return tag.value

		def decode_nbt(raw): #credit CrypticPlasma on hypixel forums, modified
			"""
			Decode a gziped and base64 decoded string to an NBT object
			"""

			return nbt.nbt.NBTFile(fileobj=io.BytesIO(raw))

		items = []
		toDecode = []

		toDecode.append(util.getVal(playerData, ['player','stats','Pit','profile','inv_contents','data'])) #inventory
		toDecode.append(util.getVal(playerData, ['player','stats','Pit','profile','inv_enderchest','data'])) #enderchest
		toDecode.append(util.getVal(playerData, ['player','stats','Pit','profile','item_stash','data'])) #stash
		toDecode.append(util.getVal(playerData, ['player','stats','Pit','profile','spire_stash_inv','data'])) #spire stash
		toDecode.append(util.getVal(playerData, ['player','stats','Pit','profile','inv_armor','data'])) #armor
		toDecode.append(util.getVal(playerData, ['player','stats','Pit','profile','mystic_well_item','data'])) #mystic well item
		toDecode.append(util.getVal(playerData, ['player','stats','Pit','profile','mystic_well_pants','data'])) #mystic well pants
		
		for curDecode in toDecode:
			if curDecode != None:
				temp = []
				for x in curDecode:
					if x < 0:
						temp.append(x + 256)
					else:
						temp.append(x)
				decoded = decode_nbt(bytes(temp))
				for tagl in decoded.tags:
					for tagd in tagl.tags:
						try:
							unpacked = unpack_nbt(tagd)
							if unpacked != {}:
								items.append(unpacked)
						except Exception as e:
							print(e)
							pass

		return items
	except Exception as e:
		print(e)
		print('error getItems')
		return []