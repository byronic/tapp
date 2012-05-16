# OBJECT class definition
#  Defines a generic game object.
#  Versatile enough to carry, use, have conversations with, ...
#  You can also think of it as an interactive object.
#
# TAPP
# COMPANY_NAME
# Byron L Lagrone
#

class OBJECT:
	# The variables that define whether an object is actionable start with _
	#      and are in the form _canAcquire, _canUse, _isSwitch, _isDoor, _canMove... etc
	#      only 'is' or 'can' and then a thing, as demonstrated ^^
	# States of an object is in the states variable, which may or may not be used depending on object
	_canAcquire = False	#Can the player pick up the object and put it into inventory?
	_canUse = False		#Can the object be used by the player (i.e. use x, wear x, put x on like it was a hat, etc
	_isConsumable = False 	#Does using the object destroy it?
	_isStatic = False	#Is the object forever bound to the room it is in? If so, we'll call it 'static'
	_inRoom = True		#Is the object not in inventory and in its origin room? ROOMDB needs this
	_canTalk = False	#Can you have a conversation with this?
	_conversationID = -99	#Conversation ID

	_description = "a generic object, surprising in its sameness."
	_word = "generic_object"# one-word object name, as it would appear in inventory or on the ground
	_roomID = -99		# the room the object is in (if _inRoom is true; otherwise ignored)

	def define(obj, word, desc, roomID): # modify an object on the fly
		obj._word = word
		obj._description = desc
		obj._roomID = roomID

	def use(obj):
		if obj._canUse:
			print "You used the object!"
		else:
			print "Oh no! You can't use that object."

	def acquire(obj):
		if obj._canAcquire:
			obj._inRoom = False
			return True
		else:
			return False

#note that talk is a standalone method, containing all of its logic internally
	def talk(obj): # try to have conversation with object
		if obj._canTalk:
			if obj._conversationID == -99:
				print "You talked to " + obj._word +", but only about politics."
			return 0 #we had a conversation! 0 is the generic successful return code
		else:
			return -1 #unsuccessful!
