import discord, json
from discord.ext import tasks, commands
from pkgs.DBCog import DBCog
from pkgs.GlobalDB import GlobalDB
from functools import wraps

def SkipCheck(func):
    @wraps(func)
    async def wrapper(self, ctx, *args, **kwargs):
        if not await self.app.is_owner(ctx.author): return
        if ctx.channel.id != self.DB['ControlTowerID']: return
        await ctx.message.delete()
        return await func(self, ctx, *args, **kwargs)
    return wrapper

class Core(DBCog):
    def __init__(self, app):
        self.CogName = 'Studio'
        DBCog.__init__(self, app)

    def initDB(self):
        self.DB = dict()
        self.DB['StudioID'] = 795704108047925289
        self.DB['ControlTowerID'] = None
        self.DB['MemberRoleID'] = None
        self.DB['UserRoleID'] = None

    @commands.command(name = 'controltowerhere')
    async def SetControlTower(self, ctx):
        if not await self.app.is_owner(ctx.author): return
        await ctx.message.delete()
        self.DB['ControlTowerID'] = ctx.channel.id
        await ctx.send('Now this channel is control tower')

    @commands.command(name = 'setstudiorole')
    @SkipCheck
    async def SetStudioRole(self, ctx, which, what):
        self.DB[f'{which}RoleID'] = self.mention2role(what, ctx.guild).id
        await ctx.send('%s role is <@&%d>'%(which, self.DB[f'{which}RoleID']))

    @commands.Cog.listener()
    async def on_ready(self):
        self.UserRoleGiver.start()

    @tasks.loop(minutes = 10.0)
    async def UserRoleGiver(self):
        Studio = self.app.get_guild(self.DB['StudioID'])
        UserRole = Studio.get_role(self.DB['UserRoleID'])
        MemberRole = Studio.get_role(self.DB['MemberRoleID'])
        async for member in Studio.fetch_members(limit = None):
            if MemberRole not in member.roles: continue
            isUser = False
            async for guild in self.app.fetch_guilds(limit = None):
                if guild == Studio: continue
                if await guild.fetch_member(member.id):
                    isUser = True
                    break
            if isUser: await member.add_roles(UserRole)
            else: await member.remove_roles(UserRole)
