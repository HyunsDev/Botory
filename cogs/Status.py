import discord, asyncio
from discord.ext import commands
from pkgs.DBCog import DBCog

class Core(DBCog):
    def __init__(self, app):
        self.CogName = 'Status'
        DBCog.__init__(self, app)

    def initDB(self):
        self.DB = dict()
        self.DB['AllCount'] = None
        self.DB['MemberCount'] = None

    @commands.group(name = 'status')
    @commands.has_guild_permissions(administrator = True)
    async def StatusGroup(self, ctx):
        await ctx.message.delete()
        if ctx.invoked_subcommand == None:
            await ctx.channel.send('Status Manager\n'
                + 'Subcommands : setup')

    @StatusGroup.command(name = 'setup')
    async def StatusSetup(self, ctx, CategoryID):
        MemberRole = discord.utils.get(ctx.guild.roles, name = '멤버')
        SetupCategory = discord.utils.get(ctx.guild.categories, id = int(CategoryID))
        self.DB['AllCount'] = await SetupCategory.create_voice_channel('전체 멤버 - 측정중🔄')
        self.DB['MemberCount'] = await SetupCategory.create_voice_channel('정식 멤버 - 측정중🔄')
        while True:
            AllCount = MemberCount = 0
            async for member in ctx.guild.fetch_members(limit = None):
                AllCount += 1
                if MemberRole in member.roles: MemberCount += 1
            await self.DB['AllCount'].edit(name = f'전체 멤버 - {AllCount}명')
            await self.DB['MemberCount'].edit(name = f'정식 멤버 - {MemberCount}명')
            await asyncio.sleep(60 * 10)

    @StatusGroup.command(name = 'update')
    async def StatusSetup(self, ctx, ChannelID, value):
        channel = discord.utils.get(ctx.guild.channels, id = int(ChannelID))
        ChannelName = channel.name
        fr = to = 0
        for i in range(len(ChannelName) - 1, -1, -1):
            if ChannelName[i].isdigit():
                to = i + 1
                break
        for i in range(to - 1, -1, -1):
            if not ChannelName[i].isdigit():
                fr = i + 1
                break
        NewName = ChannelName[:fr] + value + ChannelName[to:]
        await channel.edit(name = NewName)
        await ctx.channel.send(embed = discord.Embed(title = '서버 현황 업데이트', description = f'{ChannelName} -> {NewName[fr:]}'))
