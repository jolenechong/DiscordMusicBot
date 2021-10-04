import os
import discord
import music
from replit import db
from keep_alive import keep_alive
from bs4 import BeautifulSoup
import requests
import random
import json
from discord.ext import commands

TOKEN = ''
# add token here^^
bot = discord.Client()

# name of these  functions are said by discord
# Scrapes transcript data from dadjokes website
# we use this function in $joke command
def url_to_transcript(url):
    page = requests.get(url).text
    soup = BeautifulSoup(page, "html.parser")
    # beautiful soup to read as html file
    text = [p.text for p in soup.find(class_="card-content").find_all('p')]
    return text[0]

@bot.event
async def on_ready():
  print('bot is running, logged in as {0.user}'.format(bot))

sad_words = ['sad', 'depressed','depressing','unhappy','angry']


bot = commands.Bot(command_prefix='$')
cogs = [music]
for i in range(len(cogs)):
  cogs[i].setup(bot)    

@bot.command(name='commands')
async def commands(message):
  await message.channel.send("\nMAIN\n---\n$compliment\n$joke\n$spongebob\n\nMUSIC\n---\n$join\n$leave\n$play\n$queue [link from yt]\n$pause\n$resume")
  
@bot.command(name='joke')
async def joke(message):
  await message.channel.send("here's a dumb joke for you")
  await message.channel.send(url_to_transcript(' https://icanhazdadjoke.com/'))
  return

@bot.event
async def on_message(message):
  user_message = message.content.lower()
  username = str(message.author).split('#')[0]
  channel = str(message.channel.name)
  msg = message.content
  # print(username, ":", user_message, channel)

  if message.author == bot.user:
    return

  if user_message.startswith('hello'):
    await message.channel.send("helloo")
  
  #bot says cheer up whenever any word in sad_words list shows up in chat
  if any(word in msg for word in sad_words):
    await message.channel.send('cheer up!')

  if user_message.startswith('$note'):
    await message.channel.send("note added!")
    note = msg[6:-4]
    key = msg[-4:]
    db[key] = note
    
  if user_message.startswith('$list'):
    key = msg[-4:]
    value = db[key]
    await message.channel.send(value)

  #gets random number and refers to the list of spongebob images and displays one according to the random number
  if user_message.startswith('$spongebob'):
    spongebobIMGs = ['https://i.ibb.co/GcMrS3D/Screenshot-2021-09-05-224845.png',
                             'https://i.redd.it/we0se221hlk21.jpg',
                             'https://i.ibb.co/FJFj61b/spongebob1.png',
                             'https://preview.redd.it/y0ipdktx2ps51.jpg?width=960&crop=smart&auto=webp&s=30db61a5f0fe8f9413aa28a232ed4ccba49434f2',
                             'https://i.ibb.co/njkjmsB/spongebob2.png',
                             'https://i.ibb.co/QKm0HmK/spongebob3.png',
                             'https://i.ibb.co/YXxvj6r/spongebob4.png',
                             'https://i.ibb.co/zxmXv97/spongebob5.png',
                             'https://i.ibb.co/zJNGkV7/spongebob6.png',
                             'https://i.ibb.co/GMnJskd/spongebob7.png']

    randomNum = random.randint(1,len(spongebobIMGs)+1)
    await message.channel.send(spongebobIMGs[randomNum])

  #bot to pull data from insult api
  if user_message.startswith('$compliment'):
    await message.channel.send("here's a perfect compliment for u")
    result = requests.get('https://evilinsult.com/generate_insult.php?lang=en&type=json')
    data = result.text
    parse_json = json.loads(data)
    final_result = parse_json['insult']
    await message.channel.send(final_result)  
    
  await bot.process_commands(message)    
  
bot.run(TOKEN)
