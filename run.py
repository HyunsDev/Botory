import discord, sys, os, pickle
from discord.ext import commands
import cogs

app = commands.Bot(command_prefix = '&', intents = discord.Intents.all())

def main():
    cogs = InitCogs()
    app.run(GetToken())
    for cog in cogs: cog.saveDB()

def InitCogs():
    res = []
    for CogName in cogs.__all__:
        __import__(f'cogs.{CogName}')
        res.append(sys.modules[f'cogs.{CogName}'].Core(app))
    return res

def GetToken():
    if os.path.isfile('token.db'):
        with open('token.db', 'rb') as f: return pickle.load(f)
    token = input('Enter token : ')
    with open('token.db', 'wb') as f: pickle.dump(token, f)
    return token

@app.event
async def on_ready():
    await app.change_presence(activity = discord.Game('Botory 2.0.0 by Undec'))

if __name__ == "__main__": main()
