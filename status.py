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
        while True:
            print('this')
            acnt = cnt = 0
            ms = ctx.guild.members
            for m in ms:
                for rl in m.roles:
                    if rl.name == '멤버':
                        cnt += 1
                        break
            await ccnl.edit(name='📊서버 멤버 - %d명'%cnt)
