import discord
from discord.ext import commands
from pkgs.DBCog import DBCog
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
        if message.author.bot: return
        if len(message.attachments) and self.DB['ImageChannel']:
            if not await self.isTarget(message): return
            ImageChannel = message.guild.get_channel(self.DB['ImageChannel'])
            TinyEmbed = await self.GenAuthorEmbed(message.author)
            OrigEmbed = await self.GenAuthorEmbed(message.author)
            MessageContent = message.content
            for attachment in message.attachments[:2]:
                TinyEmbed.description = '[Button Loading]'
                TinyEmbed.set_thumbnail(url = attachment.url)
                TinyImageMessage = await message.channel.send(MessageContent, embed = TinyEmbed)
                MessageContent = ''
                OrigEmbed.description = f'[돌아가기]({TinyImageMessage.jump_url})'
                OrigEmbed.set_image(url = attachment.url)
                OriginalImageMessage = await ImageChannel.send(embed = OrigEmbed)
                TinyEmbed.description = f'[원본]({OriginalImageMessage.jump_url})'
                await TinyImageMessage.edit(embed = TinyEmbed)
            await message.delete()

    async def isTarget(self, message):
        for attachment in message.attachments:
            width, height = attachment.width, attachment.height
            if width:
                if height >= width * 0.8 or width > 150 or height > 150: return True
        return False

    async def GenAuthorEmbed(self, author):
        DisplayName = author.nick if author.nick else author.name
        embed = discord.Embed()
        embed.set_author(name = DisplayName, icon_url = str(author.avatar_url))
        return embed
