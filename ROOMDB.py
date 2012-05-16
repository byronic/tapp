# Byron L Lagrone
# python module for Text Adventure project
# here is a basic room class
#  which, by the way, now works as intended! 4/28/2012 or thereabouts ;)

from OBJECT import OBJECT
from INVENTORY import INVENTORY

# here is a test object set; you can refer to it in main if needed by using ROOMDB.OBJECTDB[0].whatever
# To add more objects, add an OBJECT() to the OBJECTDB = [ definition, and then define it in the list. The game will take care of the rest. Note the room ID must be valid, or your object never shows up.
# IMPORTANT NOTE: THE FIRST THING YOU PASS TO DEFINE (word) MUST BE ALL LOWER CASE.
# 			TODO: ^^^^^^^^^^^^^ fix the lower case requirement so that people names make sense
OBJECTDB = [ OBJECT(), OBJECT(), OBJECT(), OBJECT() ]
OBJECTDB[0].define("cat", "a cat, apparently answering to Muffin", 94)
OBJECTDB[0]._canAcquire = True
OBJECTDB[1].define("tree", "a tree, unwilling to bend to your 'rules'", 94)
OBJECTDB[2].define("pineapple", "a pineapple, ready for anything", 94)
OBJECTDB[2]._canAcquire = True
OBJECTDB[3].define("alice", "an Alice, ostensibly charming", 0)
OBJECTDB[3]._canTalk = True
OBJECTDB[3]._conversationID = -99

class ROOMDB:
#note that these are default values for example game
# also note that these are static variables
	roomID = 7 #the current room
	prevID = 7 #the previous room
	exits = ['west','north','east', 'dennis'] # human-readable
	exitIDs = [0, 3, 2, 94] #these correspond to exits[0,1...n]
	description = "You are standing in a dark room. Obvious exits are {0}, {1}, {2} and {e}.".format(exits[0], exits[1], exits[2], e=exits[3])
	objects = []
#TODO: Check to see if there is a way to automagically
#      iterate through all possible exits, i.e.
#      "...{0}, {1}, ... and {exits.length}"
	@staticmethod
	def go(_exit):
		for (counter, txt) in enumerate(ROOMDB.exits):
			if txt == _exit:
				_returner = ROOMDB.exitIDs[counter]
				ROOMDB.change(ROOMDB.exitIDs[counter])
				return _returner
		return -1 #Room IDs must be >= 0, so -1 indicates
                          #    the parse did not find a valid room

	@staticmethod
	def change(rID):
		ROOMDB.selectobjects(rID)
		if rID == 0:
			ROOMDB.exits = ['east']
			ROOMDB.exitIDs = [7];
			ROOMDB.description = "The glorious trappings of a recently vacated fairy tea party are in residence here. The only exit is {0}.".format(ROOMDB.exits[0])
#note that you could use the following model to simulate additional
#   choices for doors: exits = ['door', 'south'] 
#   exitIDs = [7, 7]
		elif rID == 3:
			ROOMDB.exits = ['door', 'gnarled']
			ROOMDB.exitIDs = [7, 7];
			ROOMDB.description = "The skeller room is packed to the brim with skellingtons. All in all, you aren't too surprised. The only exit is a gnarled door."
		elif rID == 2:
			ROOMDB.exits = ['west']
			ROOMDB.exitIDs = [7]
			ROOMDB.description = "The fairy shrine here emanates light and what you assume to be happiness. You experience a mild light-headedness in this room. Altogether: pleasant. The obvious exit is west."
		elif rID == 94:
			ROOMDB.exits = ['back']
			ROOMDB.exitIDs = [7]
			ROOMDB.description = "Dennis stands here, looking bewildered. Your only option is to go back."
		elif rID == 7:
			ROOMDB.exits = ['west','north','east', 'dennis']
			ROOMDB.exitIDs = [0, 3, 2, 94]
			ROOMDB.description = "You are standing in a dark room. Obvious exits are {0}, {1}, {2} and {e}.".format(ROOMDB.exits[0], ROOMDB.exits[1], ROOMDB.exits[2], e=ROOMDB.exits[3])
		else:
			ROOMDB.exits = ['none']
			ROOMDB.exitIDs = [-1]
			ROOMDB.description = "An error has occurred! You have arrived at an invalid room ID. Perhaps you are playing with commands or are a developer, but more likely you were fiddling around and got caught. For shame!"
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

#TODO: bug here due to OBJECTDB iteration when it should be ROOMDB.objects iteration
#       experimentally made the change
#       How is it changing in ROOMDB? Current behavior does not match with current code
#BUG: 1) Object appears to acquire successfully but is still shown as in the room;
#           To fix, remove the object from the ROOMDB.objects list
#BUG: 2) Since we are only changing it in ROOMDB.objects (which _should be_ frequently recreated -- check this!!!!!)
#           why is it not re-appearing once we exit and re-enter the room? is it getting changed
#           in the main objects database somehow? Perhaps create a sandbox branch to test with verbose debugging?
	@staticmethod
	def get(objword): #if an object is in the room and acquirable, returns True, otherwise returns False!
		for (counter, obj) in enumerate(ROOMDB.objects):
			if objword == obj._word:
				if obj._inRoom and obj._canAcquire:
					ROOMDB.objects[counter]._inRoom = False
					ROOMDB.objects[counter]._roomID = -99
					return counter
		return -99
	
# if(go to string is exit[0] (NORTH)) set active room to exitID[0] (i.e. 59 or w/e)

#TODO: Define a getter/setter (or IDs for) room exits
# here's an interesting idea:
# create a port(id) function,
#    which would teleport you to the specified id
# primarily you need 'describe'
