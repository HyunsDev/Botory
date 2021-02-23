import discord, asyncio
from discord.ext import commands
from pkgs.GlobalDB import GlobalDB
from pkgs.DBCog import DBCog
from pkgs.Scheduler import *

class Core(DBCog):
    def __init__(self, app):
        self.CogName = 'Banisher'
        self.ModRoleNames = ['경찰', '검찰', '의원']
        DBCog.__init__(self, app)

    def initDB(self):
        self.DB = dict()

    @commands.Cog.listener()
    async def on_ready(self):
        StoryGuild = self.app.get_guild(GlobalDB['StoryGuildID'])
        whoid_list = []
        for whoid in self.DB:
            if self.DB[whoid]['expire_at']: whoid_list.append(whoid)
        whoid_list.sort(key = lambda whoid: self.DB[whoid]['expire_at'].value)
        for whoid in whoid_list:
            who = StoryGuild.get_member(whoid)
            if self.DB[who.id]['expire_at'].is_done():
                await self._forgive(None, who)
                continue
            time_left = self.DB[who.id]['expire_at'].time_left()
            await asyncio.sleep(time_left.to_secs())
            await self._forgive(StoryGuild.get_channel(self.DB[who.id]['channel']), who)

    @commands.command(name = 'banish')
    @commands.has_guild_permissions(administrator = True)
    async def Banish(self, ctx, who):
        if ctx.guild.id != GlobalDB['StoryGuildID']: return
        await ctx.message.delete()
        who = self.mention2member(who, ctx.guild)
        if await self._banish(ctx, who) != 'skip':
            embed = discord.Embed(title = '', description = f'<@{who.id}> 님을 유배했습니다.')
            await ctx.channel.send(embed = embed)

    @commands.command(name = 'tempbanish')
    @commands.has_guild_permissions(administrator = True)
    async def TempBanish(self, ctx, who, duration):
        if ctx.guild.id != GlobalDB['StoryGuildID']: return
        await ctx.message.delete()
        who = self.mention2member(who, ctx.guild)
        if await self._banish(ctx, who) != 'skip':
            self.DB[who.id]['expire_at'] = Schedule(duration)
            embed = discord.Embed(title = '', description = f'<@{who.id}> 님을 {Duration(duration).to_kortext()}동안 유배했습니다.')
            await ctx.channel.send(embed = embed)
            await asyncio.sleep(Duration(duration).to_secs())
            await self._forgive(ctx.channel, who)

    @commands.command(name = 'forgive')
    @commands.has_guild_permissions(administrator = True)
    async def Forgive(self, ctx, who):
        if ctx.guild.id != GlobalDB['StoryGuildID']: return
        await ctx.message.delete()
        who = self.mention2member(who, ctx.guild)
        await self._forgive(ctx.channel, who)

    async def _banish(self, ctx, who):
        if who.id in self.DB:
            embed = discord.Embed(title = '', description = f'<@{who.id}> 님은 이미 유배중입니다.')
            await ctx.channel.send(embed = embed)
            return 'skip'
        nick = who.nick
        if who.nick == None: await who.edit(nick = '[유배중] ' + who.name)
        else: await who.edit(nick = '[유배중] ' + who.nick)
        roles = []
        for role in who.roles:
            if role.name in self.ModRoleNames:
                roles.append(role)
        await who.remove_roles(*roles[::-1])
        roles = list(map(lambda role: role.id, roles))
        self.DB[who.id] = {'channel' : ctx.channel.id, 'nick' : nick, 'roles' : roles, 'expire_at' : None}

    async def _forgive(self, channel, who):
        if who.id not in self.DB:
            embed = discord.Embed(title = '', description = f'<@{who.id}> 님은 유배중이 아닙니다.')
            await channel.send(embed = embed)
        else:
            StoryGuild = self.app.get_guild(GlobalDB['StoryGuildID'])
            nick = self.DB[who.id]['nick']
            roles = []
            for role_id in self.DB[who.id]['roles']:
                role = StoryGuild.get_role(role_id)
                roles.append(role)
            del self.DB[who.id]
            await who.edit(nick = nick)
            await who.add_roles(*roles)
            embed = discord.Embed(title = '', description = f'<@{who.id}> 님을 복직시켰습니다.')
            await channel.send(embed = embed)
