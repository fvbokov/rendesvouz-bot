from webserver import keep_alive
import os

import discord
import re
from bs4 import BeautifulSoup
import requests
from random import randint



youtube_links = []

with open('result.txt', 'r') as f:
    string = f.read()
youtube_links = string.split('\n')

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        channel = message.channel
        if message.content.startswith('/who'):
            with open(str(randint(1, 12)) + '.png', 'rb') as f:
                picture = discord.File(f)
                await channel.send(file=picture)
        if message.content.startswith('/roll'):
            if message.content == '/roll':
                await channel.send('{0.author} rolls {1}'.format(message, randint(0, 100)))
            else:
                regex = re.compile('^/roll ([0-9]+)-([0-9]+)$')
                match = regex.match(message.content)
                
                if match is None:
                    await channel.send('Wrong input. Example of correct input: "/roll 89-777"')
                    return
                else:
                    await channel.send('{0.author} rolls {1}'.format(message, randint(int(match.group(1)), int(match.group(2)))))
        if message.content == '/flip':
            n = randint(0, 1)
            if n == 0:
                await channel.send('{0.author} flips HEADS'.format(message))
            else:
                await channel.send('{0.author} flips TAILS'.format(message))
        if message.content == '/anekdot':
            s=requests.get('https://www.anekdot.ru/random/anekdot/')
            b=BeautifulSoup(s.text, "html.parser")
            p = b.find_all(class_="text")
            c = str(p[0].contents)
            c = c.replace(', <br/>,', "")
            c = c.replace('\'', "")
            c = c.replace('[', "")
            c = c.replace(']', "")
            await channel.send(c)
        if message.content == '/yt':
            url = youtube_links[randint(0, len(youtube_links)-1)]
            await channel.send(url)


client = MyClient()

#Bottom of Main.py
keep_alive()

TOKEN = os.environ['DISCORD_BOT_SECRET']

client.run(TOKEN)