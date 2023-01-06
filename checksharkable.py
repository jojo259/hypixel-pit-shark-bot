import util

def itemSharkable(curItem):

	itemNonce = util.getVal(curItem, ['tag','ExtraAttributes','Nonce'])
	itemPitEnchants = util.getVal(curItem, ['tag','ExtraAttributes','CustomEnchants'])
	itemTier = util.getVal(curItem, ['tag','ExtraAttributes','UpgradeTier'])
	itemId = util.getVal(curItem, ['id'])

	if itemTier == 0 or itemTier == 3:
		return

	if itemNonce == None:
		return

	if itemNonce >= 0 and itemNonce <= 16:
		return

	if itemPitEnchants == None:
		return

	if len(itemPitEnchants) == 3:
		return

	itemSharkable = False

	swordsLookFor = ['streak_xp', 'melee_heal_on_hit', 'melee_execute', 'melee_lightning']

	for curEnchant in itemPitEnchants:
		enchantKey = curEnchant.get('Key')
		if itemId == 283 and enchantKey in swordsLookFor:
			itemSharkable = True

	if not itemSharkable:
		return

	return True