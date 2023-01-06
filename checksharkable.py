import util

def itemSharkable(curItem):

	itemNonce = util.getVal(curItem, ['tag','ExtraAttributes','Nonce'])
	itemPitEnchants = util.getVal(curItem, ['tag','ExtraAttributes','CustomEnchants'])
	itemTier = util.getVal(curItem, ['tag','ExtraAttributes','UpgradeTier'])
	itemId = util.getVal(curItem, ['id'])

	if itemId != 283:
		return

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

	for curEnchant in itemPitEnchants:
		enchantKey = curEnchant.get('Key')
		if enchantKey == 'streak_xp' or enchantKey == 'melee_heal_on_hit':
			itemSharkable = True

	if not itemSharkable:
		return

	return True