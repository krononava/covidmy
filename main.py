import discord
import requests
import os
from keep_alive import keep_alive
import json

def getIndex(dict, country):
    for c in dict:
        if 'country' in c and country == c['country']:
            return(dict.index(c))

def getApi(i):
    params = dict(
        limit = 195
    )
    r = requests.get('https://api.coronatracker.com/v5/analytics/dailyNewStats', params = params)
    all = r.json()
    final = getIndex(all, 'Malaysia')
    if i == 'dailyCases':
        return(all[final]['daily_cases'])
    elif i == 'dailyDeath':
        return(all[final]['daily_deaths'])
    elif i == 'lastUpdated':
        return(all[final]['last_updated'])

def checkCases():
    if getApi("dailyCases") != 0:
        initial = getApi("dailyCases")
        while True:
            current = getApi("dailyCases")
            if initial == current:
                return False                                
            else:
                initial = getApi("dailyCases")
                return True

def jsonDuplicate():
    f = open('channel.json', 'r')
    data = json.load(f)
    if message.channel.id in data:
        return True
    else:
        return False

def writeJson():
    channel = None
    channel.append(message.channel.id)
    with open('channel.json', 'r') as file:
        data = json.load(file)
    data.append(channel)
    with open('channel.json', 'w') as file:
        json.dump(data, file)

def removeJson():
    with open('channel.json', 'r') as file:
        data = json.load(file)
    data.pop(message.channel.id, "not registered")
    with open('channel.json', 'w') as file:
        json.dump(data, file)

def autoSend():
    f = open('channel.json', 'r')
    data = json.load(f)
    for i in data:
        if (message.channel.id == i): 
            message.channel.send(embed = CoronaEmbed)
    f.close()

client = discord.Client()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("`awakenmycovid"):
        if (jsonDuplicate() == True):
            await message.channel.send("channel auto updates already set")
        else:
            CoronaEmbed = discord.Embed(title="The Coconut Destiny", description="[Daily Report of Covid-19](https://www.coronatracker.com/country/malaysia/)", color=0xff0000)
            CoronaEmbed.add_field(name="Cases :", value=getApi('dailyCases'), inline=False)
            CoronaEmbed.add_field(name="Death :", value=getApi('dailyDeath'), inline=False)
            CoronaEmbed.add_field(name="Last Updated :", value=getApi('lastUpdated'), inline=False)
            await message.channel.send("auto updates enabled")
            await message.channel.send(embed = CoronaEmbed)
            writeJson()

    if message.content.startswith("`slumbermycovid"):
        removeJson()
        await message.channel.send("auto updates disabled")

    if (checkCases() == True):
        autoSend()
	
keep_alive()
client.run(os.environ['token'])