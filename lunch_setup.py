import os.path

import restaurant
import restaurant_manager
import person_manager

def writeOutRestaurants(restaurant_manager):
	restaurant_manager.addRestaurant(restaurant.Restaurant.fromName("Cape of Good Hope"))
	restaurant_manager.addRestaurant(restaurant.Restaurant.fromName("Cocos"))	
	restaurant_manager.saveRestaurants()

def writeOutPeople(person_manager):
	person_manager.addPerson('thk123')
	person_manager.savePeople()

def runSetup(restaurant_manager, person_manager):
	if not os.path.isfile(restaurant_manager.restaurantsFile):
		print "Running first time setup for restaurants"
		writeOutRestaurants(restaurant_manager)
	else:
		print "Loading restaurants"
		restaurant_manager.loadRestaurants()

	if not os.path.isfile(person_manager.person_file):
		print "Running first time setup for people`"
		writeOutPeople(person_manager)
	else:
		print "Loading people"
		person_manager.loadPeople()