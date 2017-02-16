import requests
import json
import asyncio
from const import MISC

paramName = ""
paramRealm = ""

def process(subtree, messageDAO):
    global paramName, paramRealm

    key = "usage" if len(subtree) == 0 else subtree[0]
    
    try:
        paramName = subtree[1]
    except:
        return usage()
    
    try:
        paramRealm = subtree[2]
    except:
        paramRealm = MISC.DEFAULT_REALM
    
    return processCall(key,messageDAO)
    
    
def processCall(key,messageDAO):  
    if key == "relics":
        return relics(messageDAO)
    elif key == "traits":
        return traits(messageDAO)
    elif key == "ilvl":
        return ilvl(messageDAO)
    else:
        return usage()
    

def usage():
    return "usage: `!bot api <command> <username> <optional:realm, default:" + MISC.DEFAULT_REALM + ">`"

def ilvl(messageDAO):
    n = messageDAO.author.name
    print(paramName)
    print(paramRealm)

    url = 'https://'+MISC.DEFAULT_SERVER+'.api.battle.net/wow/character/' + paramRealm + "/" + paramName

    params = dict(
        fields="items",
        locale="en_GB",
        apikey="rm4g62eungjsvppyupebwsubeafrb6a9"
    )

    resp = requests.get(url=url, params=params)
    data = json.loads(resp.content)
    ilvl = data['items']['averageItemLevel']

    return 'iLvl for: **' + paramRealm+"/" + paramName + "**:`" + str(ilvl) + "`"

def relics(messageDAO):
    n = messageDAO.author.name
    print(paramName)
    print(paramRealm)

    url = 'https://'+MISC.DEFAULT_SERVER+'.api.battle.net/wow/character/' + paramRealm + "/" + paramName

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

    completemsg = 'Relics for: **' + paramRealm+"/"+paramName + '** ```'

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

def traits(messageDAO):
    totalranks = 0
    url = 'https://'+MISC.DEFAULT_SERVER+'.api.battle.net/wow/character/' + paramRealm + "/" + paramName
    params = dict(
        fields="items",
        locale="en_GB",
        apikey="rm4g62eungjsvppyupebwsubeafrb6a9"
    )

    resp = requests.get(url=url, params=params)
    data = json.loads(resp.content)
    ilvl = data['items']['averageItemLevel'] 

    if(len(data['items']['mainHand']['artifactTraits']) > 0):
        traits = data['items']['mainHand']['artifactTraits']
    else:
        traits = data['items']['offHand']['artifactTraits']
  
    for member in traits:
        totalranks += member['rank']

    #await client.send_message(channel, "Found a total of **" + str(totalranks) + "** points spent.")
    #await client.edit_message(msg, "Processing spellIDs. Will take some seconds.")

    f = open('lookup/traits.json', 'r')
    a = f.read()
    lookupdict = json.loads(a)
    f.close()

    totalranks -= 3
    completemsg = 'Traits for: **'  + paramRealm+"/"+paramName + '** (**' + str(totalranks) + ' points spent**) \n' + '```'

    for member in traits:
        url = 'https://eu.api.battle.net/wow/spell/' + str(lookupdict[str(member['id'])][0])

        params = dict(
            locale="en_GB",
            apikey="rm4g62eungjsvppyupebwsubeafrb6a9"
        )

        resp = requests.get(url=url, params=params)
        data = json.loads(resp.content)
        traitname = data['name']
        completemsg += traitname + " w/ rank: " + str(member['rank']) + "\n"
    
    
    return completemsg+"```"