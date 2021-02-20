import discord
from discord.ext import commands
import levelsys


cogs = [levelsys]

intents=intents=discord.Intents.all()
intents = discord.Intents()
intents.members = True

client = commands.Bot(command_prefix='*')

client.remove_command('help')

for i in range(len(cogs)):
  cogs[i].setup(client)


client.run("TOKEN")