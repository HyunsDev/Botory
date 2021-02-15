import discord, uuid
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

    @commands.command(name = 'imagehere')
    @commands.has_guild_permissions(administrator = True)
    async def ImageHere(self, ctx):
        await ctx.message.delete()
        self.DB['ImageChannel'] = ctx.channel.id

    @commands.Cog.listener('on_message')
    async def CompImage(self, message):
        if message.author.bot or message.author.guild_permissions.administrator: return
        if message.channel.id in getGlobalDB('IgnoreChannels'): return
        if len(message.attachments) and self.DB['ImageChannel']:
            ImageChannel = message.guild.get_channel(self.DB['ImageChannel'])
            attachment = message.attachments[0]
            if not await self.isTarget(attachment): return

            TinyEmbed = await self.GenAuthorEmbed(message.author, '[Button Loading]')
            TinyEmbed.set_thumbnail(url = attachment.url)
            TinyImageMessage = await message.channel.send(message.content, embed = TinyEmbed)

            OrigEmbed = await self.GenAuthorEmbed(message.author, f'[돌아가기]({TinyImageMessage.jump_url})[]({message.author.id})')
            OrigEmbed.set_image(url = attachment.url)
            OriginalImageMessage = await ImageChannel.send(embed = OrigEmbed)
            await OriginalImageMessage.add_reaction('❌')

            TinyEmbed.description = f'[원본보기]({OriginalImageMessage.jump_url})[]({message.author.id})'
            await TinyImageMessage.edit(embed = TinyEmbed)
            await TinyImageMessage.add_reaction('❌')
            await message.delete()

    @commands.Cog.listener('on_reaction_add')
    async def DelImage(self, reaction, user):
        if reaction.emoji != '❌': return
        if reaction.message.author.id != self.app.user.id: return
        if user.id != int(reaction.message.embeds[0].description.split('(')[-1][:-1]): return
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
        embed = discord.Embed(description = description)
        embed.set_author(name = DisplayName, icon_url = str(author.avatar_url))
        return embed
