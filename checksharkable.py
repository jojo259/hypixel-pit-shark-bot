import util

desiredEnchantsAny = [
	'melee_hidden_jewel',
]

desiredEnchantsSwords = [
	'streak_xp',
	'melee_heal_on_hit',
	'melee_execute',
	'melee_lightning',
	'melee_gamble',
	'melee_literally_p2w',
	'gold_strictly_kills',
]

desiredEnchantsSwordsTokensTwo = [
	'melee_damage_vs_diamond',
]

desiredEnchantsPants = [
	'power_against_crits',
	'regen_when_hit',
]

desiredEnchantsBows = [
	'bow_slow',
	'telebow',
	'instant_shot',
	'volley',
	'bow_combo_speed',
	'bow_weakness_on_hit',
	'punch_once_in_a_while',
	'pin_down',
]

desiredEnchantCombinations = [
	['melee_heal_on_hit', 'melee_damage_when_low']
]

desiredEnchantsTier3 = [
	'melee_lightning',
	'melee_execute',
	'melee_heal_on_hit',
	'melee_literally_p2w',
	'instant_shot',
]

desiredEnchantCombinationsTier3 = [
	['bow_slow', 'instant_shot']
]

def getItemMatchedSharkableFilters(curItem):

	itemId = util.getVal(curItem, ['id'])

	if itemId != 261 and itemId != 283 and itemId != 300:
		return []

	itemTier = util.getVal(curItem, ['tag','ExtraAttributes','UpgradeTier'])

	#if itemTier != 2:
	#	return []

	itemNonce = util.getVal(curItem, ['tag','ExtraAttributes','Nonce'])

	if itemNonce == None:
		return []

	if itemNonce >= 0 and itemNonce <= 16:
		return []

	itemPitEnchants = util.getVal(curItem, ['tag','ExtraAttributes','CustomEnchants'])

	if itemPitEnchants == None:
		return []

	if len(itemPitEnchants) == 3:
		return []

	itemPitEnchantsKeys = list(map(lambda x: x.get('Key'), itemPitEnchants))

	matchedFilters = []

	for curEnchant in itemPitEnchants:

		enchantKey = curEnchant.get('Key')
		enchantLevel = curEnchant.get('Level')

		desiredFilters = {
			'any': itemTier == 2 and enchantKey in desiredEnchantsAny,
			'bowAny': itemTier == 2 and itemId == 269 and enchantKey in desiredEnchantsBows,
			'swordAny': itemTier == 2 and itemId == 283 and enchantKey in desiredEnchantsSwords,
			'pantsAny': itemTier == 2 and itemId == 300 and enchantKey in desiredEnchantsPants,
			'swordsTokensTwoPlus': itemTier == 2 and itemId == 283 and enchantKey in desiredEnchantsSwordsTokensTwo and enchantLevel >= 2,
			'tier3testany': itemTier == 3 and enchantKey in desiredEnchantsTier3,
		}

		for filterName, filterMatch in desiredFilters.items():
			if filterMatch == True:
				matchedFilters.append(filterName)

	if itemTier == 2:
		for enchantCombination in desiredEnchantCombinations:
			allFound = True
			for curEnchant in enchantCombination:
				if curEnchant not in itemPitEnchantsKeys:
					allFound = False
			if allFound:
				matchedFilters.append('combination')

	if itemTier == 3:
		for enchantCombination in desiredEnchantCombinationsTier3:
			allFound = True
			for curEnchant in enchantCombination:
				if curEnchant not in itemPitEnchantsKeys:
					allFound = False
			if allFound:
				matchedFilters.append('combinationTier3')

	return matchedFilters