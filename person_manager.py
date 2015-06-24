

class PersonManager:
	people = set()

	person_file = "people.txt"

	def loadPeople(self):
		with open(self.person_file, 'r') as f:
			for line in f:
				self.people.add(line.rstrip('\n'))

	def savePeople(self):
		with open(self.person_file, 'w') as f:
			for person in self.people:
				f.write(person + "\n")

	def addPerson(self, person):
		if person not in self.people:
			self.people.add(person)
			return True
		else:
			return False

	def removePerson(self, person):
		if person in self.people:
			self.people.remove(person)
			return True
		else:
			return False