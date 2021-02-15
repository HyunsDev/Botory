import discord, asyncio
from discord.ext import commands

class Core(commands.Cog):
    def __init__(self, app):
        self.app = app
        self.app.add_cog(self)

    def saveDB(self): pass

    @commands.Cog.listener()
    async def on_ready(self):
        await self.app.change_presence(activity = discord.Game('Botory 2.1.0 by Undec'))
        self.guild = self.app.guilds[0]
        self.MemberRole = discord.utils.get(self.guild.roles, name = '멤버')
        perms = self.MemberRole.permissions
        perms.update(add_reactions = True, attach_files = True)
        await self.MemberRole.edit(permissions = perms)

    @commands.command(name = 'stop')
    @commands.has_guild_permissions(administrator = True)
    async def StopApp(self, ctx):
        await ctx.message.delete()
        perms = self.MemberRole.permissions
        perms.update(add_reactions = False, attach_files = False)
        await self.MemberRole.edit(permissions = perms)
        await ctx.channel.send('장비를 정지합니다.')
        await self.app.change_presence(status = discord.Status.offline)
        await asyncio.sleep(1)
        await self.app.close()
