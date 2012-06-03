# ROOMDB
#
# contains:
#   1. ROOMDB class definition
#   2. comprehensive game object database (OBJECTDB)
#   3. a need for seriously improved documentation
#
# TAPP
# Tidy Productions / Shiny Bitter Studios
# Byron L Lagrone
# Mike Robertson

from OBJECT import OBJECT
from INVENTORY import INVENTORY

# here is a test object set; you can refer to it in main if needed by using ROOMDB.OBJECTDB[0].whatever
# To add more objects, add an OBJECT() to the OBJECTDB = [ definition, and then define it in the list. The game will take care of the rest. Note the room ID must be valid, or your object never shows up.
# IMPORTANT NOTE: THE FIRST THING YOU PASS TO DEFINE (word) MUST BE ALL LOWER CASE.
# 			TODO: ^^^^^^^^^^^^^ fix the lower case requirement so that people names make sense
OBJECTDB = [ OBJECT(), OBJECT(), OBJECT(), OBJECT(), OBJECT() ]
OBJECTDB[0].define("cat", "a cat, apparently answering to Muffin", 94, 0)
OBJECTDB[0]._canAcquire = True
OBJECTDB[1].define("tree", "a tree, unwilling to bend to your 'rules'", 94, 1)
OBJECTDB[2].define("pineapple", "a pineapple, ready for anything", 94, 2)
OBJECTDB[2]._canAcquire = True
OBJECTDB[3].define("alice", "an Alice, ostensibly charming", 0, 3)
OBJECTDB[3]._canTalk = True
OBJECTDB[3]._conversationID = -99
OBJECTDB[4].define("hammock", "Joe the hammock", 3, 4)
OBJECTDB[4]._canTalk = True
OBJECTDB[4]._canAcquire = True


class ROOMDB:
#note that these are default values for example game
# also note that these are static variables
	roomID = 7 #the current room
	prevID = 7 #the previous room
	exits = ['west','north','east', 'dennis'] # human-readable
	exitIDs = [0, 3, 2, 94] #these correspond to exits[0,1...n]
	locks = [2, 0, 0, 0] #these correspond to exits [0,1...n] and define what object the player needs to unlock the door or 0 if it is unlocked already
#TODO: << BYRON NOTE :: THIS HAS BEEN DONE MINUS THE KEYRING. REDOCUMENT. >> Thoughts re: locking a room. Add a locks[] list corresponding to exitIDs/exits and check for the necessary object in the player's inventory or keyring. -- should the keyring be separate?? -- so you would have, say, locks[4] instead of a static locks[total number of rooms in the game] and if locks is non-zero it could be the OBJECTDB object number for easy checks. So, example:
#	exitIDs = [1, 2, 3]
#       locks = [0, 0, 41] # meaning 0 = unlocked, nonzero = OBJECTDB index of object that unlocks the door or indicates it is unlocked
#	Then, in go(_exit), add code that checks the lock as part of the iteration
#	Then, in main, add code that spits a verbose message if the door was locked instead of nonexistent
	description = "You are standing in a dark room. Obvious exits are {0}, {1}, {2} and {e}.".format(exits[0], exits[1], exits[2], e=exits[3])
	objects = []
#TODO: Check to see if there is a way to automagically
#      iterate through all possible exits, i.e.
#      "...{0}, {1}, ... and {exits.length}"
	@staticmethod
	def go(_exit):
		if _exit == "back":
			ROOMDB.change(ROOMDB.prevID)
			print "\nYou retrace your steps..."
			return ROOMDB.roomID	
		for (counter, txt) in enumerate(ROOMDB.exits):		
			if txt == _exit:
				if (ROOMDB.locks[counter] == 0):
					_returner = ROOMDB.exitIDs[counter]
					ROOMDB.change(ROOMDB.exitIDs[counter])
					return _returner
				elif INVENTORY.hasObject(ROOMDB.locks[counter]):
					print "\nYou unlocked the " + ROOMDB.exits[counter] + " exit with the " + INVENTORY.getObjectWord(ROOMDB.locks[counter]) + "!\n\n"
					_returner = ROOMDB.exitIDs[counter]
					ROOMDB.change(ROOMDB.exitIDs[counter])
					return _returner
				else:
					return -2 # locked and the user doesn't have the key!
		return -1 #Room IDs must be >= 0, so -1 indicates
                          #    the parse did not find a valid room

	@staticmethod
	def change(rID):
		ROOMDB.prevID = ROOMDB.roomID
		ROOMDB.roomID = rID
		ROOMDB.selectobjects(rID)
		if rID == 0:
			ROOMDB.exits = ['east']
			ROOMDB.exitIDs = [7];
			ROOMDB.description = "The glorious trappings of a recently vacated fairy tea party are in residence here. The only exit is {0}.".format(ROOMDB.exits[0])
			ROOMDB.locks = [0]
#note that you could use the following model to simulate additional
#   choices for doors: exits = ['door', 'south'] 
#   exitIDs = [7, 7]
		elif rID == 3:
			ROOMDB.exits = ['door', 'gnarled']
			ROOMDB.exitIDs = [7, 7];
			ROOMDB.description = "The skeller room is packed to the brim with skellingtons. All in all, you aren't too surprised. The only exit is a gnarled door."
			ROOMDB.locks = [0, 0]
		elif rID == 2:
			ROOMDB.exits = ['west']
			ROOMDB.exitIDs = [7]
			ROOMDB.description = "The fairy shrine here emanates light and what you assume to be happiness. You experience a mild light-headedness in this room. Altogether: pleasant. The obvious exit is west."
			ROOMDB.locks = [0]
		elif rID == 94:
			ROOMDB.exits = ['back']
			ROOMDB.exitIDs = [7]
			ROOMDB.description = "Dennis stands here, looking bewildered. Your only option is to go back."
			ROOMDB.locks = [0]
		elif rID == 7:
			ROOMDB.exits = ['west','north','east', 'dennis']
			ROOMDB.exitIDs = [0, 3, 2, 94]
			ROOMDB.description = "You are standing in a dark room. Obvious exits are {0}, {1}, {2} and {e}.".format(ROOMDB.exits[0], ROOMDB.exits[1], ROOMDB.exits[2], e=ROOMDB.exits[3])
			ROOMDB.locks = [2, 0, 0, 0]
		else:
			ROOMDB.exits = ['none']
			ROOMDB.exitIDs = [-1]
			ROOMDB.description = "An error has occurred! You have arrived at an invalid room ID. Perhaps you are playing with commands or are a developer, but more likely you were fiddling around and got caught. For shame!"
			ROOMDB.locks = [0]
		#needless to say, this concludes the definition for change(rID)

	@staticmethod
	def selectobjects(rID): #finds the objects in the room and adds them to the local objects[] list
		#TODO: Decide if this is worth keeping in its own function or if it's just as readable up there
		#first, clear the objects list
		ROOMDB.objects = []
		for (counter, obj) in enumerate(OBJECTDB):
			if obj._inRoom:
				if obj._roomID == rID:
					ROOMDB.objects.append(OBJECTDB[counter])
			else: #this is to test, please remove
				print "_inRoom is false, somehow, for " + obj._word

	@staticmethod
	def get(objword): #if an object is in the room and acquirable, sets related object package and returns True, otherwise returns False!
		for (counter, obj) in enumerate(ROOMDB.objects):
			if objword == obj._word:
				if obj._inRoom and obj._canAcquire:
					returner = ROOMDB.objects[counter]._GUID
					# for testing:
					OBJECTDB[returner]._inRoom = False
					OBJECTDB[returner]._roomID = -99
					
# added ROOMDB.objects.pop(counter) to resolve objects-in-room-description after being picked up bug
# BUG: TODO: check to see if changing return counter to return ROOMDB.objects[counter].GUID (space in objects database)
#            and don't forget that the objects database might not be correctly changing _inRoom and _roomID vals
# TODO: Check efficiency of this
					ROOMDB.objects.pop(counter)
					return returner
		return -99
	
# if(go to string is exit[0] (NORTH)) set active room to exitID[0] (i.e. 59 or w/e)

#TODO: Define a getter/setter (or IDs for) room exits
# here's an interesting idea:
# create a port(id) function,
#    which would teleport you to the specified id
# primarily you need 'describe'
