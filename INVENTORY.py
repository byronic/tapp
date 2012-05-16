# INVENTORY class definition
#  The player's inventory, because players like to pick things up
#  and use them.
#
# TAPP
# COMPANY_NAME
# Byron L Lagrone
#

#handles storage of player inventory; no logic
class INVENTORY:
	_objects = []

	@staticmethod
	def describe():
	#"""displays human-readable inventory"""
		print ""
		if len(INVENTORY._objects) == 0:
			print "You aren't carrying anything right now, excepting your over-inflated\nsense of self-worth."
		else:
			print "You are inexplicably carrying:"
			for(counter, obj) in enumerate(INVENTORY._objects):
				if counter != 0 and counter % 3 == 0:
					print ""
				print obj._word + "\t",
			print ""
			print ""

	@staticmethod
	def add(obj):
#"""where obj is an OBJECT, adds to INVENTORY's objects list"""
		INVENTORY._objects.append(obj)

	@staticmethod
	def rm(word):
#"""removes an OBJECT from inventory, if it exists."""
		for(counter, obj) in enumerate(INVENTORY._objects):
			if obj._word == word:
				INVENTORY._objects.pop(counter)
				return True
		return False
		
