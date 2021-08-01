import discord
import logging
import json
import os
import datetime
from flask import Flask
from threading import Thread
from discord.ext import tasks
from itertools import cycle

app = Flask(__name__)


@app.route('/')
def main():
    return "ready"


def run():
    app.run(host="0.0.0.0", port=8000)


def keep_alive():
    server = Thread(target=run)
    server.start()


logging.basicConfig(level=logging.ERROR) # basic logging cuz disk space

#### set up logging to a file
# logger = logging.getLogger('discord')
# logger.setLevel(logging.INFO)
# handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
# handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
# logger.addHandler(handler)
#### end

data = json.load(open("data.json"))
try:
    BOT_TOKEN = os.environ['BOT_TOKEN']  # get bot token (VERY SECRET!!!)
except KeyError:
    logging.log(
        logging.ERROR,
        "No Discord bot token detected. Are you trying to run this program without setting BOT_TOKEN?"
    )
PREFIX = "?"


class Client(discord.Client):
    status = cycle([PREFIX + "help", "Minecraft", "Potato Eating Simulator", "with the Discord API"])

    async def on_message(self, message):
        # print('Message from {0.author}: {0.content}'.format(message))
        content = message.content
        if content.startswith(PREFIX):
            # print("taking action")
            command = content.lstrip(PREFIX).split()
            # print("Command:", command)
            if command[0] == "help":
                await message.channel.send(data['help'])
            elif command[0] == "info":
                await message.channel.send(data['info'])
            else:
                if command[0] in data:
                    await message.channel.send(data[command[0]])
                else:
                    await message.channel.send(f"Unknown command. Type {PREFIX}help for help.")

    @tasks.loop(seconds=10.0)
    async def change_status(self):
        game = discord.Game(next(self.status), start = datetime.datetime(2007, 5, 1))
        await client.change_presence(status=discord.Status.online,
                                     activity=game)

    async def on_ready(self):
        self.change_status.start()
        print('Logged on as @{0}'.format(self.user))
    
    async def on_disconnect(self):
        logging.log(logging.ERROR, "Disconnected from Discord")
    
    async def on_connect(self):
        logging.log(logging.INFO, "Connected to Discord")

client = Client()
if __name__ == "__main__": 
    keep_alive() # start server for Uptime Robot
    client.run(BOT_TOKEN)
