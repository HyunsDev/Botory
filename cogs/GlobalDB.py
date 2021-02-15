import discord
from discord.ext import commands
from pkgs.DBCog import DBCog
from functools import wraps

GlobalCore = None

def getGlobalDB(key):
    return GlobalCore.DB[key]

class Core(DBCog):
    def __init__(self, app):
        self.CogName = 'GlobalDB'
        DBCog.__init__(self, app)
        global GlobalCore
        GlobalCore = self

    def initDB(self):
        self.DB = dict()
        self.DB['IgnoreChannels'] = []

    @commands.command(name = 'ignorehere')
    @commands.has_guild_permissions(administrator = True)
    async def SetIgnore(self, ctx):
        await ctx.message.delete()
        self.DB['IgnoreChannels'].append(ctx.channel.id)

    @commands.command(name = 'watchhere')
    @commands.has_guild_permissions(administrator = True)
    async def UnsetIgnore(self, ctx):
        await ctx.message.delete()
        self.DB['IgnoreChannels'].remove(ctx.channel.id)
