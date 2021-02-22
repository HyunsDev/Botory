import discord, uuid, os
from PIL import Image
from discord.ext import commands
from pkgs.DBCog import DBCog
from cogs.GlobalDB import getGlobalDB
from datetime import datetime, timezone, timedelta

class Core(DBCog):
    def __init__(self, app):
        self.CogName = 'ImageCompressor'
        DBCog.__init__(self, app)

    def initDB(self):
        self.DB = dict()
        self.DB['ImageChannel'] = None
        self.DB['IgnoreChannels'] = set()

    @commands.group(name = 'image')
    @commands.has_guild_permissions(administrator = True)
    async def ImageGroup(self, ctx):
        await ctx.message.delete()
        if ctx.invoked_subcommand == None:
            await ctx.channel.send('Automatic reactor.\nSubcommands : here, ignore')

    @ImageGroup.command(name = 'here')
    async def ImageHere(self, ctx):
        self.DB['ImageChannel'] = ctx.channel.id

    @ImageGroup.command(name = 'ignore')
    async def IgnoreHere(self, ctx):
        self.DB['IgnoreChannels'].add(ctx.channel.id)

    @ImageGroup.command(name = 'watch')
    async def WatchHere(self, ctx):
        self.DB['IgnoreChannels'].remove(ctx.channel.id)

    @commands.Cog.listener('on_message')
    async def CompImage(self, message):
        if message.author.bot or message.author.guild_permissions.administrator: return
        if message.channel.id in getGlobalDB('IgnoreChannels'): return
        if message.channel.id in self.DB['IgnoreChannels']: return
        if len(message.attachments) > 0 and self.DB['ImageChannel']:
            ImageChannel = message.guild.get_channel(self.DB['ImageChannel'])
            attachment = message.attachments[0]
            if not await self.isTarget(attachment): return

            OrigEmbed = await self.GenAuthorEmbed(message.author, '[Button Loading]')
            OriginalImageMessage = await ImageChannel.send(embed = OrigEmbed, file = await attachment.to_file())
            await OriginalImageMessage.add_reaction('❌')

            TinyEmbed = await self.GenAuthorEmbed(message.author, f'[원본보기]({OriginalImageMessage.jump_url})')
            TinyEmbed.set_thumbnail(url = OriginalImageMessage.attachments[0].url)
            TinyImageMessage = await message.channel.send(message.content, embed = TinyEmbed)
            await TinyImageMessage.add_reaction('❌')

            OrigEmbed.description = f'[돌아가기]({TinyImageMessage.jump_url})'
            await OriginalImageMessage.edit(embed = OrigEmbed)
            await message.delete()

    @commands.Cog.listener('on_reaction_add')
    async def DelImage(self, reaction, user):
        if reaction.emoji != '❌': return
        if str(user.id) != reaction.message.embeds[0].url.split('/')[-1]: return
        jump_url = reaction.message.embeds[0].description.split('(')[1].split(')')[0]
        channel_id = int(jump_url.split('/')[-2])
        message_id = int(jump_url.split('/')[-1])
        guild = self.app.guilds[0]
        channel = guild.get_channel(channel_id)
        message = await channel.fetch_message(message_id)
        await reaction.message.delete()
        await message.delete()

    async def isTarget(self, attachment):
        TempFileName = uuid.uuid4().hex
        if '.' in attachment.filename: TempFileName += '.' + attachment.filename.split('.')[-1]
        await attachment.save(TempFileName, use_cached = True)
        res = None
        try:
            Image.open(TempFileName)
            res = True
        except: res = False
        os.remove(TempFileName)
        return res

    async def GenAuthorEmbed(self, author, description):
        DisplayName = author.nick if author.nick else author.name
        embed = discord.Embed(url = f'http://www.{uuid.uuid4().hex}.com/{author.id}', description = description)
        embed.set_author(name = DisplayName, icon_url = str(author.avatar_url))
        return embed
