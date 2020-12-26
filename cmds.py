from db import *
from discord.ext import commands

class Core(commands.Cog):
    def __init__(self, app):
        self.app = app

    @commands.command(name = 'set')
    async def setcnl(self, ctx, arg):
        global dc
        await ctx.message.delete()
        if ctx.guild not in dc: dc[ctx.guild] = GuildData(ctx.guild)
        if ctx.author.top_role.name != "서버장": return
        if arg in ['report', 'rankonly', 'emojilog']:
            dc[ctx.guild].cnls[arg] = ctx.channel
            await ctx.channel.send('%s channel set here'%arg, delete_after=1.0)

    @commands.command(name = 'ignorehere')
    async def addig(self, ctx):
        global dc
        await ctx.message.delete()
        if ctx.guild not in dc: dc[ctx.guild] = GuildData(ctx.guild)
        if ctx.author.top_role.name != "서버장": return
        dc[ctx.guild].cnls.ignore.append(ctx.channel)
        await ctx.channel.send('This channel will be ignored', delete_after=1.0)

    @commands.command(name = 'checkhere')
    async def delig(self, ctx):
        global dc
        await ctx.message.delete()
        if ctx.guild not in dc: dc[ctx.guild] = GuildData(ctx.guild)
        if ctx.author.top_role.name != "서버장": return
        dc[ctx.guild].cnls.ignore.remove(ctx.channel)
        await ctx.channel.send('This channel will NOT be ignored anymore', delete_after=1.0)

    @commands.command(name = "reactauto")
    async def reactauto(self, ctx, who, what):
        global dc
        await ctx.message.delete()
        if ctx.guild not in dc: dc[ctx.guild] = GuildData(ctx.guild)
        if ctx.author.top_role.name != "서버장": return
        who = discord.utils.get(ctx.guild.members, id = int(who[3:-1]))
        dc[ctx.guild].reaction_macro[who] = what
        
    @commands.command(name = "reactoff")
    async def reactoff(self, ctx, who):
        global dc
        await ctx.message.delete()
        if ctx.guild not in dc: dc[ctx.guild] = GuildData(ctx.guild)
        if ctx.author.top_role.name != "서버장": return
        if who == "all": dc[ctx.guild].reaction_macro = dict()
        else:
            who = discord.utils.get(ctx.guild.members, id = int(who[3:-1]))
            del dc[ctx.guild].reaction_macro[who]
