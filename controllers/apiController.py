import requests
import json
import asyncio
from const import MISC
from const import PATHS
from const import TOKENS

paramName = ""
paramRealm = ""

def process(subtree, messageDAO):
    key = "usage" if len(subtree) == 0 else subtree[0]
    
    try:
        paramName = subtree[1]
    except:
        return usage()
    
    try:
        paramRealm = subtree[2]
    except:
        paramRealm = MISC.DEFAULT_REALM
    
    charParams = {'name':paramName, 'realm':paramRealm}
    return processCall(key, charParams)
    
    
def processCall(key, charParams):  
    if key == "relics":
        return getRelics(charParams)
    elif key == "traits":
        return getTraits(charParams)
    elif key == "ilvl":
        return getIlvl(charParams)
    else:
        return usage()
    

def usage():
    return "usage: `!bot api <command> <username> <optional:realm, default:" + MISC.DEFAULT_REALM + ">`"

def getIlvl(charParams):
    url = 'https://' + MISC.DEFAULT_SERVER + "." + PATHS.WOW_API_CHARACTER_URL + charParams['realm'] + "/" + charParams['name']

    params = dict(
        fields="items",
        locale="en_GB",
        apikey= TOKENS.BNET_API_KEY
    )

    resp = requests.get(url=url, params=params)
    data = json.loads(resp.content)
    ilvl = data['items']['averageItemLevel']

    return 'iLvl for: **' + charParams['realm'] + "/" + charParams['name'] + "**:`" + str(ilvl) + "`"

def getRelics(charParams):
    url = 'https://' + MISC.DEFAULT_SERVER + "." + PATHS.WOW_API_CHARACTER_URL + charParams['realm'] + "/" + charParams['name']
    print(url)
    params = dict(
        fields="items",
        locale="en_GB",
        apikey= TOKENS.BNET_API_KEY
    )

    resp = requests.get(url=url, params=params)
    data = json.loads(resp.content)
    ilvl = data['items']['averageItemLevel'] 

    if(len(data['items']['mainHand']['relics']) > 0):
        relics = data['items']['mainHand']['relics']
    else:
        relics = data['items']['offHand']['relics']

    completemsg = 'Relics for: **' + charParams['realm'] + "/" + charParams['name'] + '** ```'

    for relic in relics:
        url =  'https://' + MISC.DEFAULT_SERVER + "." + PATHS.WOW_API_ITEM_URL + str(relic['itemId'])

        params = dict(
            locale="en_GB",
            apikey="rm4g62eungjsvppyupebwsubeafrb6a9"
        )

        resp = requests.get(url=url, params=params)
        data = json.loads(resp.content)
        relicname = data['name']
        completemsg += relicname + "\n"

    return completemsg + "```"

def getTraits(charParams):
    totalranks = 0
    url = 'https://' + MISC.DEFAULT_SERVER + "." + PATHS.WOW_API_CHARACTER_URL + charParams['realm'] + "/" + charParams['name']

    params = dict(
        fields="items",
        locale="en_GB",
        apikey= TOKENS.BNET_API_KEY
    )

    resp = requests.get(url=url, params=params)
    data = json.loads(resp.content)

    if(len(data['items']['mainHand']['artifactTraits']) > 0):
        traits = data['items']['mainHand']['artifactTraits']
    else:
        traits = data['items']['offHand']['artifactTraits']
  
    for trait in traits:
        totalranks += trait['rank']

    lookupFile = open('lookup/traits.json', 'r')
    lookupContent = lookupFile.read()
    lookupFile.close()

    lookupDict = json.loads(lookupContent)
    
    totalranks -= 3
    completemsg = 'Traits for: **'  + charParams['realm'] + "/" + charParams['name'] + '** (**' + str(totalranks) + ' points spent**) \n' + '```'

    for trait in traits:
        url = 'https://eu.api.battle.net/wow/spell/' + str(lookupDict[str(trait['id'])][0])

        params = dict(
            locale="en_GB",
            apikey="rm4g62eungjsvppyupebwsubeafrb6a9"
        )

        resp = requests.get(url=url, params=params)
        data = json.loads(resp.content)
        traitname = data['name']
        completemsg += traitname + " w/ rank: " + str(trait['rank']) + "\n"
    
    
    return completemsg + "```"