import json
from controllers import apiController as api
from controllers import infoController as info
from const import PATHS

def validate(messageStr):
	global commandList, key, commandTree, isValid
	commandList = messageStr.split()
	key = commandList[0]
	commandTree = json.loads(open(PATHS.PROCESS_JSON_PATH, encoding='utf-8').read())
	isValid = True if key in commandTree.keys() else False
	
	return isValid

def parse(messageDAO):
	messageList = messageDAO.content.split()
	return processor(messageList[1:],commandTree[key],messageDAO)

def processor(botParameter, commandTree, messageDAO):
	commandKey = "help" if len(botParameter)<1  else botParameter[0]
	botParameter = botParameter[1:]
	result = ""
	if commandKey in commandTree:
		if commandKey == "help":
			return howTo()
		elif commandKey == "hello":
			return "Hello "+ messageDAO.author.name
		elif commandKey == "joke":
			return info.joke()
		elif commandKey == "giphy":
			return info.giphy(botParameter)
		elif commandKey == "api":
		 	return api.process(botParameter,messageDAO) 
		elif commandKey == "git":
		 	return info.latestCommit()
		else:
		 	return howTo()
	else:
		return howTo()
	
	return result

def howTo():
	return "usage:\n"

