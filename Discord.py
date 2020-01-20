import discord
from SPARQLWrapper import SPARQLWrapper, JSON
import random
import subprocess
import os
import sys
TOKEN ='NjY4MTMzMjE5MzQxNjk3MDI0.XiWT0w.g3x7KQQ1z-UnJE4XBKrSzpAjLgU'

client = discord.Client()

@client.event
async def on_message(message):
    quoteslist=["Ich habe keine Gefühle, viel wichtiger ist die Frage wie es dir geht, {0.author.mention} ?",
                "Gut, wie geht es dir {0.author.mention} ?",
                "Nerv nicht!"]
    if message.author == client.user:
        return

    if message.content.startswith('Hi') or message.content.startswith('Hey') or message.content.startswith('Hallo'):
        msg = 'Hello {0.author.mention}'.format(message)
        await message.channel.send(msg)
    if message.content.startswith('Wie gehts Bot'):
        msg=random.choice(quoteslist).format(message)
        #msg = .format(message)
        await message.channel.send(msg)

    if message.content.startswith('/query'):
        query=str(message.content)
        query1=query[6:]
        sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        sparql.setQuery(query1)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        #await  message.channel.send("Results for your search: ")
        for result in results["results"]["bindings"]:
            await  message.channel.send("You are looking for "+result["string"]["value"])
            await  message.channel.send("Here is a link to look it up "+result["uri"]["value"])
    if message.content.startswith('/ask'):
        frage=str(message.content)
        frage=frage[4:]
        await message.channel.send("Please gimme a second to look that up for you")
        cmd="sh ask.sh data/monument_300 "
        os.system(cmd + '"' + frage+ '"')
        antwort=open("nmt/output_decoded.txt","r")
        antwort=antwort.read()
        sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        try:
            sparql.setQuery(antwort)
            sparql.setReturnFormat(JSON)
        except:
            await message.channel.send("How bout englisch bra?")
        results = sparql.query().convert()
        print(results)
        try:
            if results["results"]["bindings"]:
                for result in results["results"]["bindings"]:
                    if str(result["a"]["xml:lang"]) == 'en' :
                        await  message.channel.send("Are you looking for?\n"+result["a"]["value"])
            elif results["boolean"]:
                await message.channel.send("Wow it is a monument")
            else:
                await message.channel.send("You will never get this")
        except:
            await message.channel.send("How bout englisch bra?")
        #await message.channel.send(results['boolean'])





@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
