from discord import Client
from controllers import commandController as commands

client = Client()

@client.event
async def on_message(messageDAO):
    if messageDAO.author == client.user:
        return
    replyObj = commands.parse(messageDAO)
    if replyObj != None:      
        await client.send_message(messageDAO.channel, replyObj)


@client.event   
async def on_ready():
    print('Logged in as')
    print(client.user.name + "("+client.user.id+")")
    print('------')


async def sendError(tb):
    print(tb)