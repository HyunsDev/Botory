from datetime import datetime, timedelta
from db import *
from discord.ext import commands

class Core(commands.Cog):
    def __init__(self, app):
        self.app = app

    @ReactorGroup.command(name = 'set')
    async def setcnl(self, ctx, arg):
        global db
        await ctx.message.delete()
        if ctx.author.top_role.name != "서버장": return
        if arg in cnlnames:
            db.cnls[arg] = ctx.channel
            await ctx.channel.send('%s channel set here'%arg, delete_after=1.0)

    @commands.command(name = 'ignorehere')
    async def addig(self, ctx):
        global db
        await ctx.message.delete()
        if ctx.author.top_role.name != "서버장": return
        db.igcnls.append(ctx.channel)
        await ctx.channel.send('This channel will be ignored', delete_after=1.0)

    @commands.command(name = 'checkhere')
    async def delig(self, ctx):
        global db
        await ctx.message.delete()
        if ctx.author.top_role.name != "서버장": return
        db.igcnls.remove(ctx.channel)
        await ctx.channel.send('This channel will NOT be ignored anymore', delete_after=1.0)

    async def dur2sec(self, duration):
        lst = [0, 0, 0, 0, 0]
        lst['smhdw'.index(duration[-1])] = int(duration[:-1])
        return timedelta(seconds=lst[0], minutes=lst[1], hours=lst[2], days=lst[3], weeks=lst[4])

    async def _setreact(self, who, whats):
        db.autoreacts[who] = dict()
        emjs = []
        for what in whats:
            what = str(what)
            if len(what) == 1: emjs.append(str(what))
            else: emjs.append(int(str(what).split(':')[2][:-1]))
        db.autoreacts[who]['emjs'] = emjs

    @commands.command(name = 'banish')
    async def banish(self, ctx, who):
        global db
        await ctx.message.delete()
        if ctx.author.top_role.name != '서버장': return
        who = m2m(who, ctx.guild)
        if who in db.banishdata: await ctx.channel.send('<@%d> 님은 이미 유배중입니다.'%who.id, allowed_mentions = discord.AllowedMentions.none(), delete_after=1.0)
        else:
            onick = who.nick
            if who.nick == None: await who.edit(nick = '[유배중] ' + who.name)
            else: await who.edit(nick = '[유배중] ' + who.nick)
            orls = []
            for rl in who.roles:
                if rl.name in adroles: orls.append(rl)
            await who.remove_roles(*orls[::-1])
            db.banishdata[who] = (onick, orls)
            await ctx.channel.send('<@%d> 님을 유배했습니다.'%who.id, allowed_mentions = discord.AllowedMentions.none(), delete_after=1.0)

    @commands.command(name = 'forgive')
    async def forgive(self, ctx, who):
        global db
        await ctx.message.delete()
        if ctx.author.top_role.name != '서버장': return
        who = m2m(who, ctx.guild)
        if who not in db.banishdata: await ctx.channel.send('<@%d> 님은 유배중이 아닙니다.'%who.id, allowed_mentions = discord.AllowedMentions.none(), delete_after=1.0)
        else:
            onick, orls = db.banishdata[who]
            del db.banishdata[who]
            await who.edit(nick = onick)
            await who.add_roles(*orls)
            await ctx.channel.send('<@%d> 님을 복직시켰습니다.'%who.id, allowed_mentions = discord.AllowedMentions.none(), delete_after=1.0)

    @commands.command(name = 'cnlupdate')
    async def cnlupdate(self, ctx, cnlid, val):
        await ctx.message.delete()
        cnl = discord.utils.get(ctx.guild.channels, id = int(cnlid[2:-1]))
        cnlname = cnl.name
        fr = to = 0
        for i in range(len(cnlname) - 1, -1, -1):
            if cnlname[i].isdigit():
                to = i + 1
                break
        for i in range(to - 1, -1, -1):
            if not cnlname[i].isdigit():
                fr = i + 1
                break
        newname = cnlname[:fr] + val + cnlname[to:]
        await cnl.edit(name = newname)
        await ctx.channel.send(embed = discord.Embed(title = '서버 현황 업데이트', description = '%s -> %s'%(cnlname, newname[fr:])))
