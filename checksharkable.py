import util

def itemSharkable(curItem):

	itemId = util.getVal(curItem, ['id'])

	if itemId != 261 and itemId != 283 and itemId != 300:
		return

	itemTier = util.getVal(curItem, ['tag','ExtraAttributes','UpgradeTier'])

	if itemTier != 2:
		return

	itemNonce = util.getVal(curItem, ['tag','ExtraAttributes','Nonce'])

	if itemNonce == None:
		return

	if itemNonce >= 0 and itemNonce <= 16:
		return

	itemPitEnchants = util.getVal(curItem, ['tag','ExtraAttributes','CustomEnchants'])

	if itemPitEnchants == None:
		return

	if len(itemPitEnchants) == 3:
		return

	itemSharkable = False

	desiredEnchantsAny = [
		'melee_hidden_jewel'
	]

	desiredEnchantsSwords = [
		'streak_xp',
		'melee_heal_on_hit',
		'melee_execute',
		'melee_lightning',
		'melee_gamble',
		'melee_damage_when_low',
		'melee_damage_vs_diamond',
		'melee_literally_p2w'
	]

	desiredEnchantsPants = [
		'power_against_crits',
		'regen_when_hit'
	]

	desiredEnchantsBows = [
		'bow_slow'
	]

	desiredEnchantCombinations = [
		['melee_heal_on_hit', 'melee_damage_when_low']
	]

	for curEnchant in itemPitEnchants:
		enchantKey = curEnchant.get('Key')
		if (enchantKey in desiredEnchantsAny) or (itemId == 269 and enchantKey in desiredEnchantsBows) or (itemId == 283 and enchantKey in desiredEnchantsSwords) or (itemId == 300 and enchantKey in desiredEnchantsPants):
			itemSharkable = True

	itemPitEnchantsKeys = list(map(lambda x: x.get('Key'), itemPitEnchants))

	for enchantCombination in desiredEnchantCombinations:
		allFound = True
		for curEnchant in enchantCombination:
			if curEnchant not in itemPitEnchantsKeys:
				allFound = False
		if allFound:
			itemSharkable = True

	return itemSharkable