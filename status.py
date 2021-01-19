import discord, asyncio
from datetime import datetime
from db import *
from discord.ext import commands

class Core(commands.Cog):
    def __init__(self, app):
        self.app = app
        self.amems = dict()

    @commands.command(name = 'setupstat')
    async def setup(self, ctx, category):
        global db
        await ctx.message.delete()
        if ctx.author.top_role.name != "서버장": return
        ctgry = discord.utils.get(ctx.guild.categories, id = int(category))
        ccnl = await ctx.guild.create_voice_channel('📊서버 멤버 - 측정중', category=ctgry)
        acnl = await ctx.guild.create_voice_channel('📊활동적인 멤버 - 측정중', category=ctgry)
        await asyncio.gather(
            asyncio.ensure_future(self.csetup(ctx, ccnl)),
            asyncio.ensure_future(self.asetup(ctx, acnl)))

    async def csetup(self, ctx, cnl):
        while True:
            cnt = 0
            for ms in ctx.guild.members:
                for rl in ms.roles:
                    if rl.name == '멤버':
                        cnt += 1
                        break
            await cnl.edit(name='📊서버 멤버 - %d명'%cnt)
            await asyncio.sleep(10)

    async def asetup(self, ctx, cnl):
        while True:
            cnt = 0
            for ms in ctx.guild.members:
                for rl in ms.roles:
                    if rl.name == '멤버':
                        cnt += 1
                        break
            await cnl.edit(name='📊활동적인 멤버 - %d명'%len(self.amems))
            await asyncio.sleep(10)

    @commands.Cog.listener()
    async def on_message(self, message):
        hsh = datetime.now()
        self.amems[message.author] = hsh
        await asyncio.sleep(60)
        if self.amems[message.author] == hsh:
            del self.amems[message.author]
