import random
import json
from pprint import pprint
dictalc = {}
#happiness, anger, sadness, contempt, disgust, fear, neutral, surprise
budget = 5
with open("alcohols.json") as file:
	alcohols = json.load(file)


#HAPPINESS
if (emotion == "happiness"):
	happinessDrinkDict = {**alcohols['Red Wine'], **alcohols['Beers']}


	lst = []
	for drink in happinessDrinkDict.keys():
		if float(happinessDrinkDict[drink]) <= float(budget):
			lst.append((drink,happinessDrinkDict[drink]))
	happyChoice = lst[random.randint(0,len(lst)-1)]

	#NEUTRAL
if(emotion == "neutral"):
	neutralDrinkDict = {**alcohols['Vodka']}

	neutralList = []
	for drink in neutralDrinkDict.keys():
		if float(neutralDrinkDict[drink]) <= float(budget):
			neutralList.append((drink, neutralDrinkDict[drink]))
	neutralChoice = neutralList[random.randint(0,len(neutralList)-1)]



#ANGER

elif(emotion == "anger"):
	angerDrinkDict = {**alcohols['White Wine']}


	angerList = []
	for drink in angerDrinkDict.keys():
		if float(angerDrinkDict[drink]) <= float(budget):
			angerList.append((drink, angerDrinkDict[drink]))
	angerChoice = angerList[random.randint(0,len(angerList)-1)]

#SADNESS


elif(emotion == "sadness"):

	sadnessDrinkDict = {**alcohols['White Wine']}


	sadnessList = []
	for drink in sadnessDrinkDict.keys():
		if float(sadnessDrinkDict[drink]) <= float(budget):
			sadnessList.append((drink, sadnessDrinkDict[drink]))
	sadnessChoice = sadnessList[random.randint(0,len(sadnessList)-1)]





