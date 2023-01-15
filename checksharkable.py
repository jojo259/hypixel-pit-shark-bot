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
]

desiredEnchantCombinations = [
	['melee_heal_on_hit', 'melee_damage_when_low']
]

def getItemMatchedSharkableFilters(curItem):

	itemId = util.getVal(curItem, ['id'])

	if itemId != 261 and itemId != 283 and itemId != 300:
		return []

	itemTier = util.getVal(curItem, ['tag','ExtraAttributes','UpgradeTier'])

	if itemTier != 2:
		return []

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
			'any': enchantKey in desiredEnchantsAny,
			'bowAny': itemId == 269 and enchantKey in desiredEnchantsBows,
			'swordAny': itemId == 283 and enchantKey in desiredEnchantsSwords,
			'pantsAny': itemId == 300 and enchantKey in desiredEnchantsPants,
			'swordsTokensTwoPlus': itemId == 283 and enchantKey in desiredEnchantsSwordsTokensTwo and enchantLevel >= 2,
		}

		for filterName, filterMatch in desiredFilters.items():
			if filterMatch == True:
				matchedFilters.append(filterName)

	for enchantCombination in desiredEnchantCombinations:
		allFound = True
		for curEnchant in enchantCombination:
			if curEnchant not in itemPitEnchantsKeys:
				allFound = False
		if allFound:
			matchedFilters.append('combination')

	return matchedFilters