import discord, sys, os, pickle
from discord.ext import commands
from pkgs import GlobalDB
import cogs

app = commands.Bot(command_prefix = '&', intents = discord.Intents.all(), help_command = None)

def main():
    GlobalDB.loadDB()
    cogs = InitCogs()
    app.run(GetToken())
    for cog in cogs: cog.saveDB()
    GlobalDB.saveDB()

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

if __name__ == "__main__": main()
