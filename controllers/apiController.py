import requests
import json
import asyncio

def process(subtree, messageDAO):
	key = "usage" if len(subtree) == 0 else subtree[0]
	subtree = subtree[1:]
	return processCall(key,messageDAO)
    
    
def processCall(key,messageDAO):
	result = ""
	if key == "tc1":
		return traits(messageDAO)
	elif key == "tc2":
		return relics()
	else:
		return usage()
	

def usage():
	return "usage:"

def traits(messageDAO):
    n = messageDAO.author.name

    url = 'https://eu.api.battle.net/wow/character/' + "thrall" + "/" + "eliath"

    params = dict(
        fields="items",
        locale="en_GB",
        apikey="rm4g62eungjsvppyupebwsubeafrb6a9"
    )

    resp = requests.get(url=url, params=params)
    data = json.loads(resp.content)
    ilvl = data['items']['averageItemLevel'] 

    if(len(data['items']['mainHand']['relics']) > 0):
        relics = data['items']['mainHand']['relics']
    else:
        relics = data['items']['offHand']['relics']

    completemsg = 'Relics for: **' + n + '** ```'

    for member in relics:
        url = 'https://eu.api.battle.net/wow/item/' + str(member['itemId'])

        params = dict(
            locale="en_GB",
            apikey="rm4g62eungjsvppyupebwsubeafrb6a9"
        )

        resp = requests.get(url=url, params=params)
        data = json.loads(resp.content)
        relicname = data['name']
        completemsg += relicname + "\n"

        #asyncio.sleep(5)
    return completemsg + "```"

def relics():
    return("asked for relics")