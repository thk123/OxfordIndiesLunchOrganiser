import json
from restaurant import Restaurant
from random import choice

class RestaurantManager:

	restaurantsFile = "restaurants.json"

	loadedRestaurants = set()

	def loadRestaurants(self):
		current_restaurants = []
		with open(self.restaurantsFile, 'r') as f:
			current_restaurants = json.load(f)

		for restaurantJson in current_restaurants:
			self.loadedRestaurants.add(Restaurant.fromJson(restaurantJson))

	def addRestaurant(self, restaurant):
		if restaurant not in self.loadedRestaurants:
			self.loadedRestaurants.add(restaurant)
			return True
		else:
			return False

	def pickRestaurant(self):
		options = []
		for restaurant in self.loadedRestaurants:
			score = restaurant.getScore()
			for i in range(0, score):
				options.append(restaurant)


		print(options)
		return choice(options)



	def saveRestaurants(self):
		restaurantJson = []
		for restaurant in self.loadedRestaurants:
			restaurantJson.append(restaurant.getJsonObject())

		with open(self.restaurantsFile, 'w') as f:
			json.dump(restaurantJson, f)

