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

	desiredEnchantsSwords = ['streak_xp', 'melee_heal_on_hit', 'melee_execute', 'melee_lightning']
	desiredEnchantsPants = ['power_against_crits']

	for curEnchant in itemPitEnchants:
		enchantKey = curEnchant.get('Key')
		if (itemId == 283 and enchantKey in desiredEnchantsSwords) or (itemId == 300 and enchantKey in desiredEnchantsPants):
			itemSharkable = True

	if not itemSharkable:
		return

	return True