import datetime

class Restaurant:
	restaurant_name = ""
	last_visit = datetime.date(year = 2015, month = 01, day = 01)

	@classmethod
	def fromName(cls, restaurant_name):
		return cls(restaurant_name, datetime.date(year = 2015, month = 01, day = 01))

	@classmethod
	def fromJson(cls, json):
		return cls(json['name'], datetime.date.fromordinal(json['lastVisit']))		

	def __init__(self, restaurant_name, last_visit):
		self.restaurant_name = restaurant_name
		self.last_visit = self.last_visit

	def getJsonObject(self):
		return {
		'name' : self.restaurant_name,
		'lastVisit' : self.last_visit.toordinal()
		}
		