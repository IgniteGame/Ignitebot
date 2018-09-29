#ignitebot#5783
#first time only: py -m pip install discord.py
#everytime: py ignitebot.py
#tutorial: https://www.devdungeon.com/content/make-discord-bot-python
#link to add to server: https://discordapp.com/oauth2/authorize?client_id=429839546977615882&scope=bot
#new bot: https://discordapp.com/developers/applications/me then new application then create bot user
#link to edit bot: https://discordapp.com/developers/applications/me

#TODO: whose rolled the most times

import discord
import random
import json
import csv
import sys
import time



VERSION = "1.2.4"

client = discord.Client()

#https://stackoverflow.com/questions/13949637/how-to-update-json-file-with-python
def addRoll(message):
	with open("rolls.json", "r+") as textfile:
		data = json.load(textfile)
		
		data["totalRolls"]+=1
		
		if str(message.author) in data:
			data[str(message.author)]+=1
		else:
			data[str(message.author)]=1
		
		textfile.seek(0)
		json.dump(data, textfile)
		textfile.truncate()
	
def getTotalRolls():
	with open("rolls.json", "r") as textfile:
		data = json.load(textfile)
		return data["totalRolls"]

def getUserRolls(message):
	with open("rolls.json", "r") as textfile:
		data = json.load(textfile)
		if str(message.author) in data:
			return data[str(message.author)]
		return "0"

def getCard(name):
	with open("decks.csv") as csvfile:
		readCSV = csv.reader(csvfile, delimiter=",")
		cardRow = None
		for row in readCSV:
			if row[1].lower().replace(" ","") == name.lower().replace(" ",""):
				cardRow = row
				break
		if cardRow != None:
			return ":name_badge: Name: **" + row[1] + "**\n:robot: Type: **" + row[2] + "**\n:zap: Cost: **" + row[3] + "**\n:wrench: Attack: **" + row[4] + "**\n:gear: Health: **" + row[5] + "**\n:fire: Ignite Rolls: **" + row[6] + "**\n:pencil2: Text: **" + row[7] + "**\n:pencil: Deck: **" + row[8] + "**"
		return "card not found"

@client.event
async def on_message(message):

	# we do not want the bot to reply to itself
	if message.author == client.user:
		return
		
	msgInfo = "Author: " + str(message.author) + ". Channel: " + str(message.channel) + ". Content: " + str(message.content) + ". Time: " + time.strftime("%H:%M:%S-%m/%d/%Y") + "\n------"
	print(msgInfo)
	
	with open("log.txt", "r+") as log:
		log.readlines()
		log.write(msgInfo+"\n")
		
	#requires that you use "!ignitebot" unless it's a dm
	if str(message.channel.type) != "private" and message.content.lower().find("!ignitebot") == -1:
		return
		
	#--------------------------------
	
	if str(message.author) == "JonnyG21#2641" and message.content == "quit":
		sys.exit()
	
	elif message.content.lower().find("help") != -1:
		msg = "type \"!ignitebot\" followed by a command. You don't need to do this part if you PM ignitebot" 
		msg += "\n\nCommands include \"help\", \"-ignite\", \"experiment\", \"smolder\", \"rolls\", and rolling a fair die, such as \"d4\" "
		msg += "\n\n You can also type \"data:\" followed by a card name to recieve its stats. For example: \"data:molten maniac\""
		msg += "\n\nVersion: " + VERSION + " :gear:"
		await client.send_message(message.channel, msg)
		
	elif message.content.lower().find("rolls") != -1:
		msg = "I've rolled " + str(getTotalRolls()) + " dice. " 
		msg += str(getUserRolls(message)) + " of them are from you. :game_die:"
		await client.send_message(message.channel, msg)
		
	elif message.content.lower().find("-ignite") != -1:
		addRoll(message)
		targets = ["slot 1", "slot 2", "slot 3", "slot 4", "forge", "forge"]
		explosions = ["small", "medium", "large"]
		explosion = random.randint(0,2)
		msg = "You hit " + random.choice(targets) + " with a " + random.choice(explosions) + " explosion :boom:"
		await client.send_message(message.channel, msg)
	
	elif message.content.lower().find("experiment") != -1:
		addRoll(message)
		rolls = [1, 2, 2, 3, 3, 4, 4, 5]
		msg = "You experimented for " + str(random.choice(rolls)) + " :zap:"
		await client.send_message(message.channel, msg)
	
	elif message.content.lower().find("smolder") != -1:
		addRoll(message)
		smolders = ["small", "medium", "medium", "large"]
		msg = "You smoldered slot " + str(random.randint(0,3)+1) + " for " + str(random.choice(smolders)) + " :fire:"
		await client.send_message(message.channel, msg)
		
	elif message.content.lower().find("data:") != -1:
		name = message.content.lower().split("data:")[1]
		msg = getCard(name)
		await client.send_message(message.channel, msg)
		
	else:
		rolled = False
		#i is startIdx, j is endIdx
		for i in range(0,len(message.content)):
			if message.content[i] == 'd' and str.isdigit(message.content[i+1]): #found something to roll
				j = i+2
				while j != len(message.content) and str.isdigit(message.content[j]): #find index of last digit
					j+=1
				numToRoll = int(message.content[i+1:j])
				msg = "rolled a d" + str(numToRoll) + ": " + str(random.randint(1,numToRoll))
				await client.send_message(message.channel, msg)
				addRoll(message)				
				rolled = True
				break
			i+=1

		if(not rolled and str(message.channel.type) == "private"):
			msg = "I didn't understand that. Type \"help\" for help"
			await client.send_message(message.channel, msg)



@client.event
async def on_ready():
	print("Logged in as")
	print("Name: " + client.user.name)
	print("ID: " + client.user.id)
	print("Version: " + VERSION)
	print("------")

with open("token.txt", "r") as tokenFile:
	TOKEN = tokenFile.readline()
	print("Token: " + TOKEN)
client.run(TOKEN)

