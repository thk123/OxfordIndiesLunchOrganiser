import twitter
import urlparse
import oauth2 as oauth
import time
from twython import Twython
import re
import app_keys as keys

import os.path

import person_manager
import restaurant_manager

from lunch_setup import runSetup


saved_tokens_path = "saved_tokens.txt"

consumer_key = keys.consumer_key
consumer_secret = keys.consumer_secret

def firstTimeLogin():
	print("Performing first time login (interactive)")
	oauthRequestUrl = "https://api.twitter.com/oauth/request_token"
	twitter = Twython(consumer_key, consumer_secret)
	auth = twitter.get_authentication_tokens(callback_url='oob')

	OAUTH_TOKEN = auth['oauth_token']
	OAUTH_TOKEN_SECRET = auth['oauth_token_secret']

	print("Go to the following URL and authorise the app (Kim and Toms app)")
	print(auth['auth_url'])
	print("Once done, enter the PIN")

	oauth_verifier = ""
	while oauth_verifier == "":
	    oauth_verifier = raw_input('What is the PIN? ')

	twitter = Twython(consumer_key, consumer_secret, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
	final_step = twitter.get_authorized_tokens(oauth_verifier)

	OAUTH_TOKEN = final_step['oauth_token']
	OAUTH_TOKEN_SECRET = final_step['oauth_token_secret']

	print("Saving tokens")

	with open(saved_tokens_path, "w") as f:
		print("Token: %s Secret: %s", OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
		f.write(OAUTH_TOKEN + "\n" + OAUTH_TOKEN_SECRET)

	return Twython(consumer_key, consumer_secret, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

def getTwitter():

	if os.path.isfile(saved_tokens_path):
		with open(saved_tokens_path, "r") as f:
			print("Reading saved tokens")
			saved_token = f.readline().rstrip('\n')
			saved_secret = f.readline().rstrip('\n')

		twitter = Twython(consumer_key, consumer_secret, saved_token, saved_secret)
		# twitter.verify_credentials()
		return twitter
	else:
		return firstTimeLogin()

# Do request





def replyToTweet(tweetToReplyTo, contentsOfTweet, twitter):
	sender = tweetToReplyTo['user']['screen_name']
	tweetId = tweetToReplyTo['id']
	status = "@" + sender + " " + contentsOfTweet

	print("Tweeting: " + status)
	# twitter.update_status(status = status, in_reply_to_status_id = tweetId)

def processAddTweet(tweet, twitter):

	contents = tweet['text']
	m = re.search('add @(\w+)$', contents)
	if m:
		print("Adding user: " + m.group(1))

		did_add_person = person_manager.addPerson(m.group(1))
		if did_add_person:
			person_manager.savePeople()
			replyToTweet(tweet, "Welcome on board @" + m.group(1) + "!", twitter)
		else:
			replyToTweet(tweet, "I already know about you, silly!", twitter)

	else:
		print("Error passsing match" + contents)
		replyToTweet(tweet, "Sorry, that isn't a valid \'add\' command", twitter)
		


def processRemoveTweet(tweet, twitter):
	contents = tweet['text']
	m = re.search('remove @(\w+)$', contents)
	if m:
		print("Removig user: " + m.group(1))

		did_remove_person = person_manager.removePerson(m.group(1))
		if did_remove_person :
			person_manager.savePeople()
			replyToTweet(tweet, "Goodbye!", twitter)
		else:
			replyToTweet(tweet, "I litterally don't know who you are...", twitter)

	else:
		print("Error passsing match " + contents)
		replyToTweet(tweet, "Sorry, that isn't a valid \'remove\' command", twitter)
			

def processAddRestaurant(tweet, twitter):

	contents = tweet['text']
	m = re.search('restaurant ([\w\s\',]+)$', contents)
	if m:
		print("adding restaurant: " + m.group(1))

		did_add_restaurant = restaurant_manager.addRestaurant(m.group(1))
		if did_add_restaurant:
			restaurant_manager.saveRestaurants()
			replyToTweet(tweet, "Ooo, good choice, I'd be salvating if I was a human", twitter)
		else:
			replyToTweet(tweet, "So good you want to add it twice?", twitter)

	else:
		print("Error passsing match " + contents)
		replyToTweet(tweet, "Sorry, that isn't a valid restaurant command", twitter)	

def processUnknownTweet(tweet, twitter):
	replyToTweet(tweet, "Sorry, I don't recognise that command, use add, remove or restaurant, cc @thk123", twitter)

twitter = getTwitter()

person_manager = person_manager.PersonManager()
restaurant_manager = restaurant_manager.RestaurantManager()

runSetup(restaurant_manager, person_manager)

latest_status_id_file = "last_status.txt"

latest_status_id = 0
if os.path.isfile(latest_status_id_file):
	with open(latest_status_id_file, 'r') as f:
		latest_status_id = long(f.read())

print("Getting all tweets after " + str(latest_status_id))

# check for new mentions
if latest_status_id > 0:
	mentions = twitter.get_mentions_timeline(since_id = str(latest_status_id))
else:
	mentions = twitter.get_mentions_timeline()

for mention in reversed(mentions):
	tweetContent = mention['text'].lower()
	print(tweetContent)
	if 'add' in tweetContent:
		print("Adding user")
		processAddTweet(mention, twitter)
	elif 'remove' in tweetContent:
		processRemoveTweet(mention, twitter)
	elif 'restaurant' in tweetContent:
		processAddRestaurant(mention, twitter)
	else:
		processUnknownTweet(mention, twitter)

	status_id = long(mention['id'])
	if status_id > latest_status_id:
		latest_status_id = status_id
		with open(latest_status_id_file, 'w') as f:
			f.write(str(latest_status_id))



# TODO: choose random restaurant (based on when last visited)
# TODO: notify all people
# TODO: update date of last visited for that pub

# TODO: Respond to requests to organise pub
# TODO: Allow people to opt-in/out of lunch/pub individually

#t = Twitter(auth = OAuth(token, token_key, con_secret, con_secret_key))


#t.statuses.update(status = "Test status")