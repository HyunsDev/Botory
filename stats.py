import os, sqlite3, discord, asyncio
from discord.ext import commands

class Core(commands.Cog):
    def __init__(self, app):
        self.app = app

    @commands.group(name = 'stats')
    async def stats(self, ctx): pass

    @stats.command(name = 'setup')
    async def setup(self, ctx, arg):
        memrl = discord.utils.get(ctx.guild.roles, name = '멤버')
        category = discord.utils.get(ctx.guild.categories, id = int(arg))
        acnl = await category.create_voice_channel('전체 멤버 - 측정중🔄')
        mcnl = await category.create_voice_channel('정식 멤버 - 측정중🔄')
        while True:
            acnt = mcnt = 0
            async for member in ctx.guild.fetch_members(limit=None):
                acnt += 1
                if memrl in member.roles: mcnt += 1
            await acnl.edit(name = f'전체 멤버 - {acnt}명')
            await mcnl.edit(name = f'정식 멤버 - {mcnt}명')
            await asyncio.sleep(60*10)

    @stats.command(name = 'export')
    async def export(self, ctx):
        if not ctx.author.guild_permissions.administrator: return
        members = await ctx.guild.fetch_members(limit=None).flatten()
        return
