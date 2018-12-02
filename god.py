from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import logging
import requests
import json
import random

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

locjson = ""
emo = ""
maptext = ""


#Registering the updater and dispatcher
updater = Updater(token='768461777:AAFE5txqPI7Rh5bkt7a5l4VndmA1LmosVbk')
dispatcher = updater.dispatcher


#For the start command
def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm Alcobot, please send your budget, picture and location to me!")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.start_polling()


#For handling the budget
def echo(bot, update):
	global bud
	bud = int(update.message.text)
	#print(bud)
	textmess = "Your budget is £" + str(update.message.text)
	bot.send_message(chat_id=update.message.chat_id, text=textmess)

echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)


#For photos
def photo(bot, update):
    file_id = update.message.photo[-1].file_id
    newFile = bot.getFile(file_id)
    newFile.download('test.jpg')
    bot.sendMessage(chat_id=update.message.chat_id, text="Got your picture mate!")
    imagerec(bot, update)

#For image classification
def imagerec(bot, update):
	url = "https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect"
	querystring = {"returnFaceId":"true","returnFaceLandmarks":"false","returnFaceAttributes":"emotion,age,gender"}

	image_path = "/Users/AkshayC/Desktop/test.jpg"
	image_data = open(image_path, "rb").read()

	headers = {
		'Ocp-Apim-Subscription-Key': "9495f13ff2764d0f87daec1d820257e8",
		'Content-Type': "application/octet-stream",
		'cache-control': "no-cache",
		'Postman-Token': "67ac9f11-e73a-430f-aca3-eb71b7dcc0a5"
		}	

	response = requests.request("POST", url, data=image_data, headers=headers, params=querystring)

	age = int(response.json()[0]["faceAttributes"]["age"])
	emotion = response.json()[0]["faceAttributes"]["emotion"]

	maxint = -0.5

	for key in emotion:
		if (emotion[key] > maxint):
			maxint = emotion[key]
			emo = key
	
	#print(maxint)
	print(emo)
	#print(age)

	print(bud)
	classify(bot, update, emo, int(bud))


photo_handler = MessageHandler(Filters.photo, photo)
dispatcher.add_handler(photo_handler)

#For the Location
def location(bot, update):

	locjson = str(str(update.message.location['latitude']) + "," + str(update.message.location['longitude']))
	print(locjson)
	#bot.sendMessage(chat_id=update.message.chat_id, text=str(update.message.location))
	loc(bot, update, locjson)


location_handler = MessageHandler(Filters.location, location, edited_updates=True)
dispatcher.add_handler(location_handler)

#For getting the map link
def loc(bot, update, locations):

	url_pubs = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
	params_pubs = {'key' : 'AIzaSyA6zIAya7DpOz8KKAKTr65tw6LNI5ktKzE',
	     'location' :  locations,
	       'rankby' : 'distance',
	        'type'  : 'pub',
	     'keyword'  : 'pubs',
	     'maxprice' : 3
	         }
	r = requests.get(url = url_pubs, params = params_pubs)

	data = r.json()
	restaurant_name = data['results'][0]['name']
	lat = data['results'][0]['geometry']['location']['lat']
	lng = data['results'][0]['geometry']['location']['lng']
	map_url = "maps.google.com/?q="+str(lat)+','+str(lng)
	maptext = "Your closest pub is " + restaurant_name + "\n" + map_url

	bot.sendMessage(chat_id=update.message.chat_id, text=maptext)


def classify(bot, update, emo, bud):
	with open("alcohols.json") as file:
		alcohols = json.load(file)
	emotion = emo
	budget = bud

	#HAPPINESS
	if (emotion == "happiness"):
		bot.sendMessage(chat_id=update.message.chat_id, text="You seem to be happy! :)")
		happinessDrinkDict = {**alcohols['Red Wine'], **alcohols['Beers']}
		lst = []
		for drink in happinessDrinkDict.keys():
			#print(float(happinessDrinkDict[drink]), float(budget))
			if float(happinessDrinkDict[drink]) <= float(budget):
				lst.append((drink,happinessDrinkDict[drink]))
		#print(lst)
		happyChoice = lst[random.randint(0,len(lst) - 1)]
		finaltext = "Your recommended drink is " + happyChoice[0] + ". The cost of a standard drink is £" + happyChoice[1] + "."
		bot.sendMessage(chat_id=update.message.chat_id, text=finaltext)
		bot.sendMessage(chat_id=update.message.chat_id, text="Please send your location too!")

	#NEUTRAL
	elif(emotion == "neutral"):
		bot.sendMessage(chat_id=update.message.chat_id, text="Seems like you're not feeling anything now")
		neutralDrinkDict = {**alcohols['Vodka']}
		neutralList = []
		for drink in neutralDrinkDict.keys():
			if float(neutralDrinkDict[drink]) <= float(budget):
				neutralList.append((drink, neutralDrinkDict[drink]))
		neutralChoice = neutralList[random.randint(0,len(neutralList)-1)]
		finaltext = "Your recommended drink is " + neutralChoice[0] + ". The cost of a standard drink is £" + neutralChoice[1] + "."
		bot.sendMessage(chat_id=update.message.chat_id, text=finaltext)
		bot.sendMessage(chat_id=update.message.chat_id, text="Please send your location too!")

	#ANGER
	elif(emotion == "anger"):
		bot.sendMessage(chat_id=update.message.chat_id, text="You seem angry! Count to 10 and you'll feel better!")
		angerDrinkDict = {**alcohols['White Wine']}
		angerList = []
		for drink in angerDrinkDict.keys():
			if float(angerDrinkDict[drink]) <= float(budget):
				angerList.append((drink, angerDrinkDict[drink]))
		angerChoice = angerList[random.randint(0,len(angerList)-1)]
		finaltext = "Your recommended drink is " + angerChoice[0] + ". The cost of a standard drink is £" + angerChoice[1] + "."
		bot.sendMessage(chat_id=update.message.chat_id, text=finaltext)
		bot.sendMessage(chat_id=update.message.chat_id, text="Please send your location too!")

	#SADNESS
	elif(emotion == "sadness"):
		bot.sendMessage(chat_id=update.message.chat_id, text="Why are you sad man? Cheer up!")
		sadnessDrinkDict = {**alcohols['White Wine']}
		sadnessList = []
		for drink in sadnessDrinkDict.keys():
			if float(sadnessDrinkDict[drink]) <= float(budget):
				sadnessList.append((drink, sadnessDrinkDict[drink]))
		sadnessChoice = sadnessList[random.randint(0,len(sadnessList)-1)]

		finaltext = "Your recommended drink is " + sadnessChoice[0] + ". The cost of a standard drink is £" + sadnessChoice[1] + "."
		bot.sendMessage(chat_id=update.message.chat_id, text=finaltext)
		bot.sendMessage(chat_id=update.message.chat_id, text="Please send your location too!")
