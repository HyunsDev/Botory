import discord, csv, uuid, os
from discord.ext import commands
from pkgs.DBCog import DBCog
from pkgs.GlobalDB import GlobalDB
from pkgs.Scheduler import *

class Core(DBCog):
    def __init__(self, app):
        self.CogName = 'Fetcher'
        DBCog.__init__(self, app)

    def initDB(self):
        self.DB = dict()

    @commands.command(name = 'fetch')
    @commands.has_guild_permissions(administrator = True)
    async def SetReact(self, ctx):
        CsvFileName = f'FetchData-{uuid.uuid4().hex}.csv'
        with open(CsvFileName, 'w', encoding = 'utf-8') as f:
            CsvWriter = csv.writer(f)
            CsvWriter.writerow(['id', 'name', 'nick', 'presence emoji', 'presence', 'presence type'])
            cnt = 0
            async for member in ctx.guild.fetch_members(limit = None):
                cnt += 1
                if cnt % 300 == 0: await ctx.send(str(cnt))
                CsvWriter.writerow([member.id, member.name, member.nick, str(member.activities)])
        await ctx.send(f'{cnt} members fetched', file = discord.File(CsvFileName))
        os.remove(CsvFileName)
