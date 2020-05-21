from discord.ext.commands import Bot

from config import Config
import botCommands

import sys
import logging


logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)


file_handler = logging.StreamHandler()
logger.addHandler(file_handler)

config = Config.from_file(file="config.json", readonly=True)
config["colour"] = {x:int(config["colour"][x], base=16) for x in config["colour"]} # converts str of colour hexs to base10 ints

client = Bot(
    command_prefix=config["bot_prefix"],
    description=config["description"],
    owner_id=config["owner_id"],
    case_insensitive=True
)
client.logger = logger
client.config = config

def setup(client):
    client.add_cog(botCommands.Events(client))
    client.add_cog(botCommands.Information(client))


if __name__ == '__main__':
    setup(client)
    client.run(sys.argv[1])
