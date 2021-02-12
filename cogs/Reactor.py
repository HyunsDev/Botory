import discord
from discord.ext import commands
from pkgs.DBCog import DBCog
from pkgs.Scheduler import *

class Core(DBCog):
    def __init__(self, app):
        self.CogName = 'Reactor'
        DBCog.__init__(self, app)

    def initDB(self):
        self.DB = dict()

    @commands.group(name = 'reactor')
    @commands.has_guild_permissions(administrator = True)
    async def ReactorGroup(self, ctx):
        await ctx.message.delete()
        if ctx.invoked_subcommand == None:
            await ctx.channel.send('Automatic reactor.\n'
                + 'Subcommands : set, tempset, unset')

    async def SetReactDB(self, who, whats):
        self.DB[who.id] = dict()
        emojis = []
        for what in whats:
            try: emojis.append(int(what.split(':')[2][:-1]))
            except: emojis.append(what)
        self.DB[who.id]['emojis'] = emojis

    @ReactorGroup.command(name = 'set')
    async def SetReact(self, ctx, who, *whats):
        who = self.mention2member(who, ctx.guild)
        await self.SetReactDB(who, whats)
        self.DB[who.id]['expire_at'] = None
        embed = discord.Embed(title = '', description = f'<@{who.id}> 님께 자동 이모지가 등록되었습니다.')
        await ctx.channel.send(embed = embed)

    @ReactorGroup.command(name = "tempset")
    async def SetTempReact(self, ctx, who, duration, *whats):
        who = self.mention2member(who, ctx.guild)
        await self.SetReactDB(who, whats)
        embed = discord.Embed(title = '', description = f'<@{who.id}> 님께 {Duration(duration).to_kortext()}동안 자동 이모지가 등록되었습니다.')
        self.DB[who.id]['expire_at'] = Schedule(duration)
        await ctx.channel.send(embed = embed)

    @ReactorGroup.command(name = "unset")
    async def UnsetReact(self, ctx, who):
        who = self.mention2member(who, ctx.guild)
        if who == "all": self.DB = dict()
        else:
            who = self.mention2member(who, ctx.guild)
            del self.DB[who.id]

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id in self.DB:
            expiration = self.DB[message.author.id]['expire_at']
            if expiration:
                if expiration.is_done():
                    del self.DB[message.author.id]
                    return
            emojis = self.DB[message.author.id]['emojis']
            for emoji in emojis:
                if type(emoji) == int: emoji = discord.utils.get(self.app.emojis, id = emoji)
                await message.add_reaction(emoji)
