import discord, sys
from discord.ext import commands
import pkgs
from pkgs import AppData

app = commands.Bot(command_prefix = '&', intents = discord.Intents.all())

def main():
    cogs = InitCogs()
    app.run(GetToken())
    for cog in cogs: cog.saveDB()

def InitCogs():
    res = []
    for module in pkgs.cogs:
        __import__(f'pkgs.{module}')
        res.append(sys.modules[f'pkgs.{module}'].Core(app))

@app.event
async def on_ready():
    await AppData.app.change_presence(activity = discord.Game('Botory 2.0.0 by Undec'))

if __name__ == "__main__": main()
