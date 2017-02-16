from discord import Client
from controllers import commandController as commands
import asyncio

client = Client()

@client.event
async def on_message(messageDAO):
    if messageDAO.author == client.user:
        return

    if(commands.validate(messageDAO.content)):
        await workinProgress(messageDAO)
        
        replyObj = commands.parse(messageDAO)   
        print(replyObj)
        if replyObj != None:  
            await client.send_message(messageDAO.channel, replyObj)
            #await client.delete_message(msgObj)

async def workinProgress(messageDAO):
    messageText = "iamworking"
    msgObj = await client.send_message(messageDAO.channel, messageText)
    for i in range(3):
        messageText+="."
        msgObj = await client.edit_message(msgObj, messageText)
        await asyncio.sleep(1)


    #await workinProgress()


@client.event   
async def on_ready():
    print('Logged in as')
    print(client.user.name + "("+client.user.id+")")
    print('------')


async def sendError(tb):
    print(tb)