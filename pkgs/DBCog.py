import discord, os, pickle, re
from discord.ext import commands

class DBCog(commands.Cog):
    def __init__(self, app):
        self.app = app
        self.loadDB()
        self.app.add_cog(self)

    def loadDB(self):
        print(f'Loading {self.CogName}.db ...')
        if os.path.isfile(f'{self.CogName}.db'):
            with open(f'{self.CogName}.db', 'rb') as f:
                self.DB = pickle.load(f)
            print(f'{self.CogName}.db loaded!')
            return
        print(f'{self.CogName}.db not found!')
        self.initDB()

    def saveDB(self):
        print(f'Saving {self.CogName}.db ...')
        with open(f'{self.CogName}.db', 'wb') as f:
            pickle.dump(self.DB, f)
        print(f'{self.CogName}.db saved!')

    def mention2member(self, mention, guild):
        member_id = int(re.sub("[^0-9]", "", mention))
        return guild.get_member(member_id)

    def mention2role(self, mention, guild):
        role_id = int(re.sub("[^0-9]", "", mention))
        return guild.get_role(role_id)
    
    async def waitforModMessage(self, channel):
        def checker(message):
            return message.author.id == self.app.owner_id and message.channel == channel
        return await self.app.wait_for('message', check = checker)

    async def waitforModReaction(self, message, emojis):
        for emoji in emojis:
            await message.add_reaction(emoji)
        def checker(reaction, user):
            return reaction.message == message and reaction.emoji in emojis and user.id == self.app.owner_id
        reaction, _ = await self.app.wait_for('reaction_add', check = checker)
        return emojis.index(reaction.emoji)

    async def MessageFromLink(self, link):
        guild_id = int(link.split('/')[-3])
        channel_id = int(link.split('/')[-2])
        message_id = int(link.split('/')[-1])
        guild = self.app.get_guild(guild_id)
        channel = guild.get_channel(channel_id)
        return await channel.fetch_message(message_id)

    def GetDisplayName(self, member):
        if member.nick: return member.nick
        return member.name
