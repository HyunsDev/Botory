import discord, uuid
from discord.ext import commands
from pkgs.GlobalDB import GlobalDB
from pkgs.DBCog import DBCog
from functools import wraps

def SkipCheck(func):
    @wraps(func)
    async def wrapper(self, message):
        if message.guild.id != GlobalDB['StoryGuildID']: return
        if message.author.bot or message.author.guild_permissions.administrator: return
        if message.channel.id in GlobalDB['IgnoreChannels']: return
        return await func(self, message)
    return wrapper

class Core(DBCog):
    def __init__(self, app):
        self.CogName = 'Filter'
        DBCog.__init__(self, app)

    def initDB(self):
        self.DB = dict()
        self.DB['ReportChannel'] = None
        self.DB['MaxLength'] = 200
        self.DB['MaxLines'] = 4

    @commands.command(name = 'setlimit')
    @commands.has_guild_permissions(administrator = True)
    async def SetLimit(self, ctx, arg):
        if ctx.guild.id != GlobalDB['StoryGuildID']: return
        await ctx.message.delete()
        if arg[-1] == 'l':
            self.DB['MaxLines'] = int(arg[:-1])
            embed = discord.Embed(title = '', description = f'줄수 제한이 {self.DB["MaxLines"]}줄이 되었습니다')
            await ctx.channel.send(embed = embed)
        else:
            self.DB['MaxLength'] = int(arg)
            embed = discord.Embed(title = '', description = f'글자수 제한이 {self.DB["MaxLength"]}글자가 되었습니다')
            await ctx.channel.send(embed = embed)

    @commands.command(name = 'reporthere')
    @commands.has_guild_permissions(administrator = True)
    async def SetChannels(self, ctx):
        if ctx.guild.id != GlobalDB['StoryGuildID']: return
        await ctx.message.delete()
        self.DB['ReportChannel'] = ctx.channel.id

    @commands.Cog.listener('on_message')
    @SkipCheck
    async def ModShouldBeOnline(self, message):
        if '경찰' in map(lambda x: x.name, message.author.roles) and message.author.status == discord.Status.offline:
            await message.channel.send(f'<@{message.author.id}> 관리자께서는 되도록이면 오프라인 상태를 해제하여 관리활동 중임을 표시해주세요.')

    @commands.Cog.listener('on_message')
    @SkipCheck
    async def NoMiddleFinger(self, message):
        if '🖕' in message.content:
            await message.delete()
            await self.MiddleFingerReport(message.author.id, message.channel)

    @commands.Cog.listener('on_message')
    @SkipCheck
    async def DontMentionMaster(self, message):
        if "서버장" in list(map(lambda x: x.top_role.name, message.mentions)):
            await message.channel.send("<@%d> 허가받은 역할멘션 외 서버장 직접 멘션은 경고조치됩니다."%message.author.id)
            if self.DB['ReportChannel']:
                ReportChannel = message.guild.get_channel(self.DB['ReportChannel'])
                await ReportChannel.send("<@%d> 이 사용자 서버장 직접멘션으로 경고바랍니다."%message.author.id, allowed_mentions = discord.AllowedMentions.none())

    # 글자 수 제한 초과, 줄 제한 초과
    @commands.Cog.listener('on_message')
    @SkipCheck
    async def LengthLimiter(self, message):
        if len(message.content) <= self.DB['MaxLength'] and message.content.count('\n') < self.DB['MaxLines']:
            return None

        LongTextChannel = message.guild.get_channel(self.DB['LongTextChannel'])

        # 사본 긴 메세지 정보
        LongMsgOrigInfoEmbed = await self.GenAuthorEmbed(message.author, '[Button Loading]')
        LongMsgOrigInfoMessage = await LongTextChannel.send(embed=LongMsgOrigInfoEmbed)
        await LongMsgOrigInfoMessage.add_reaction('❌')

        # 사본 긴 메세지
        LongMsgOrigContent = message.content
        MsgFilter = ['@'] # 맨션 테러를 막기 위해 인라인 맨션 필터링
        for i in MsgFilter:
            LongMsgOrigContent = LongMsgOrigContent.replace(i, '\\'+i)
        await LongTextChannel.send(LongMsgOrigContent)

        # 단축된 메세지
        LongMsgTinyEmbed = await self.GenAuthorEmbed(message.author, f'긴 메세지\n[내용보기]({LongMsgOrigInfoMessage.jump_url})')
        LongMsgTinyMessage = await message.channel.send(embed = LongMsgTinyEmbed, reference = message.reference)
        await LongMsgTinyMessage.add_reaction('❌')

        # 사본 긴 메세지 [돌아가기]
        LongMsgOrigInfoMessage.description = f'[돌아가기]({LongMsgTinyMessage.jump_url})'
        await LongMsgOrigInfoMessage.edit(embed = LongMsgOrigInfoEmbed)

        # 원본 삭제
        await message.delete()

    @commands.Cog.listener('on_message')
    @SkipCheck
    async def DontMentionReply(self, message):
        if message.reference != None:
            if message.reference.resolved.author in message.mentions:
                await message.channel.send('답장을 할 때는 되도록이면 오른쪽 `@켜짐`을 눌러 멘션을 꺼주세요!', delete_after = 5.0)

    @commands.Cog.listener('on_message')
    @SkipCheck
    async def DontSendMultipleFiles(self, message):
        if len(message.attachments) > 1:
            await message.channel.send('파일은 한번에 하나씩만 보내 주세요!', delete_after = 2.0)

   
    @commands.Cog.listener('on_reaction_add')
    async def DelLongMsg(self, reaction, user):
        jump_url = reaction.message.embeds[0].description.split('(')[1].split(')')[0]
        channel_id = int(jump_url.split('/')[-2])
        message_id = int(jump_url.split('/')[-1])
        guild = self.app.guilds[0]
        channel = guild.get_channel(channel_id)
        message = await channel.fetch_message(message_id)
        await reaction.message.delete()
        await message.delete()

    async def GenAuthorEmbed(self, author, description):
        DisplayName = author.nick if author.nick else author.name
        embed = discord.Embed(url = f'http://www.{uuid.uuid4().hex}.com/{author.id}', description = description)
        embed.set_author(name = DisplayName, icon_url = str(author.avatar_url))
        return embed

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if reaction.message.guild.id != GlobalDB['StoryGuildID']: return
        if user.bot or user.guild_permissions.administrator: return
        if reaction.message.channel.id in GlobalDB['IgnoreChannels']: return
        if '🖕' in str(reaction.emoji):
            await reaction.clear()
            await self.MiddleFingerReport(user.id, reaction.message.channel)

    async def MiddleFingerReport(self, UserID, channel):
        ReportChannel = channel.guild.get_channel(self.DB['ReportChannel'])
        await channel.send(f'<@{UserID}> 중지 절단 완료.')
        if ReportChannel:
            await ReportChannel.send(f'<@{UserID}> 이 사용자 중지 이모지 사용으로 경고바랍니다.', allowed_mentions = discord.AllowedMentions.none())
