import discord
from SPARQLWrapper import SPARQLWrapper, JSON
import re
TOKEN ='NjY4MTMzMjE5MzQxNjk3MDI0.XiNE7A.jPA_Z-9LUSChCu8E0pAV_2Tpqos'

client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await message.channel.send(msg)

    if message.content.startswith('/query'):
        query=str(message.content)
        query1=query[6:]
        sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        sparql.setQuery(query1)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        await  message.channel.send("Results for your search: ")
        for result in results["results"]["bindings"]:
            await  message.channel.send(result["uri"]["value"])
            await  message.channel.send(result["string"]["value"])


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)