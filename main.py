#!/usr/bin/env python

# Main entry point to TAPP
#  Contains main game loop
#
# TAPP
# COMPANY_NAME
# Byron L Lagrone
#

import ROOMDB
from INVENTORY import INVENTORY

print "Byron Lagrone proudly presents"
print "a Proof of Concept application"
print "  Text Adventure Engine Test"
print "(c) 2012"
print ""
quit = False 		# has the user quit the game?
countdownToLook = 0	# how many 'ticks' until the room description should be displayed

while quit != True:
	success = False # Was (T)the user's command successful or (F)should we display an error?
	if countdownToLook <= 0:
		countdownToLook = 5 #number of commands before looking again	
		print ROOMDB.ROOMDB.description
		if len(ROOMDB.ROOMDB.objects) == 1:
			print "You see " + ROOMDB.ROOMDB.objects[0]._description + "."
		elif len(ROOMDB.ROOMDB.objects) > 1:
			print "You see ",
			for(counter, obj) in enumerate(ROOMDB.ROOMDB.objects):
				print obj._description,
				if counter == len(ROOMDB.ROOMDB.objects) - 2:
					print "\b, and",
				elif counter == len(ROOMDB.ROOMDB.objects) - 1:
					print "\b."
				else:
					print "\b,",
	inp = raw_input(">").lower() #acquire user input and handle
	if inp == "quit":
		quit = True
		success = True
	elif inp == "exit": #possibly ambiguous command
		print "If you'd like to stop playing, type 'quit'. If you'd like to exit the room, type 'go ' followed by a room exit."
	else:
		words = inp.split() #Array of single words from inp, i.e. ["go", "west", "dumby"]
		mode = 0 # what command we are interpreting; 0 is not recognized
		for (counter, word) in enumerate(words):
			if mode == 0: #efficiency -- only check this if mode isn't already decided
				if word == "go" or word == "walk" or word=="north" or word=="south" or word=="east" or word=="west":
					mode = 1
				elif word == "inventory" or word == "inv":
					INVENTORY.describe()
					success = True
					break
				elif word == "get":
					mode = 2
				elif word == "say" or word == "talk" or word == "hail" or word == "hello" or word == "hi":
					mode = 9 #conversation time!
				elif word == "look":
					success = True
					print ""
					print "You examine your surroundings.\n"
					countdownToLook = 0
				elif word == "sudo":
					mode = -4
			if mode == 1:
				if ROOMDB.ROOMDB.go(word) >= 0: #TODO: Check efficiency of .lower()
					success = True			#TODO: better idea: lower before for
					countdownToLook = 0
					mode = 0
					break
			elif mode == 2:
				index = ROOMDB.ROOMDB.get(word)
				if index >= 0:
					success = True
					mode = 0
					INVENTORY.add(ROOMDB.OBJECTDB[index])
					break
			elif mode == 9: #converse!
				for(counter, obj) in enumerate(ROOMDB.OBJECTDB):
					if word == ROOMDB.OBJECTDB[counter]._word:
						if ROOMDB.OBJECTDB[counter].talk() >= 0:
							success = True
							break
		if success != True:
			if mode == 1:
				print "You tried to " + inp + ", but no such exit exists. Everyone was sad. Especially me."
			elif mode == 2:
				print "You tried to " + inp + ", but you couldn't acquire such a thing."
			elif mode == 9:
				print "Your attempt to " + inp + " wasn't reciprocated. \nPerhaps they're not feeling chatty..."
			else:
				print "Much to your chagrin, you can't " + inp
		countdownToLook -= 1

print "Exiting... thanks for playing!"
