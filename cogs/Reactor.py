import discord
from pkgs import DBCog, Scheduler

class Core(DBCog.DBCog):
    def __init__(self, app):
        self.CogName = 'Reactor'
        DefaultCog.Core.__init__(self, app)

    def initDB(self):
        self.DB = dict()

    @commands.group(name = 'reactor')
    @commands.has_guild_permissions(administrator = True)
    async def ReactorGroup(self, ctx):
        if ctx.invoked_subcommand == None:
            ctx.channel.send('Automatic reactor.\n'
                + 'Subcommands : set, tempset, unset')

    async def SetReactDB(self, who, whats):
        self.DB[who.id] = dict()
        emjs = []
        for what in whats:
            if len(what) == 1: emjs.append(discord.utils.get(self.app.emojis, name = what).id)
            else: emjs.append(int(what.split(':')[2][:-1]))
        self.DB[who.id]['emjs'] = emjs

    @ReactorGroup.command(name = 'set')
    async def SetReact(self, ctx, who, *whats):
        await ctx.message.delete()
        who = self.mention2member(who, ctx.guild)
        await self.SetReactDB(who, whats)
        self.DB[who.id]['tilwhen'] = None
        embed = discord.Embed(title = '', description = '<@%d> 님께 자동 이모지가 등록되었습니다.'%who.id)
        await ctx.channel.send(embed=embed)

    @ReactorGroup.command(name = "tempset")
    async def SetTempReact(self, ctx, who, duration, *whats):
        await ctx.message.delete()
        who = self.mention2member(who, ctx.guild)
        await self.SetReactDB(who, whats)
        embed = discord.Embed(title='', description = '<@%d> 님께 %d%s동안 자동 이모지가 등록되었습니다.'%(who.id,
            int(duration[:-1]), {'s':'초','m':'분','h':'시간','d':'일','w':'주'}[duration[-1]]))
        db.autoreacts[who]['tilwhen'] = datetime.now() + await self.dur2sec(duration)
        await ctx.channel.send(embed=embed)

    @ReactorGroup.command(name = "unset")
    async def UnsetReact(self, ctx, who):
        await ctx.message.delete()
        who = self.mention2member(who, ctx.guild)
        if who == "all": self.DB = dict()
        else:
            who = self.mention2member(who, ctx.guild)
            del self.DB[who.id]
