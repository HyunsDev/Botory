from db import *
from discord.ext import commands
import imagecomp

async def middle_finger_report(gld, userid, mcnl):
    global dc
    cnl = dc[gld].cnls.report
    await mcnl.send("<@%d> 중지 절단 완료."%userid)
    if cnl != None: await cnl.send("<@%d> 이 사용자 중지 이모지 사용으로 경고바랍니다."%userid, allowed_mentions = discord.AllowedMentions.none())

async def filter_message(message):
    global dc
    rcnl = dc[message.guild].cnls.report
    if message.author.top_role.name in ['서버장', '대장']: return False
    if message.channel in dc[message.guild].cnls.ignore: return False
    if '🖕' in message.content:
        await middle_finger_report(message.guild, message.author.id, message.channel)
        return True
    if "서버장" in list(map(lambda x: x.top_role.name, message.mentions)):
        await message.channel.send("<@%d> 허가받은 역할멘션 외 서버장 직접 멘션은 경고조치됩니다."%message.author.id)
        if rcnl != None: await rcnl.send("<@%d> 이 사용자 서버장 직접멘션으로 경고바랍니다."%message.author.id, allowed_mentions = discord.AllowedMentions.none())
        return True
    if message.channel == dc[message.guild].cnls.rankonly:
        if len(message.attachments): return True
        if message.content[:5] != '!rank': return True
        if len(message.mentions):
            await message.channel.send("<@%d> 멘션을 사용한 랭크명령어는 경고조치됩니다."%message.author.id, delete_after = 1.0)
            if rcnl != None: await rcnl.send("<@%d> 이 사용자 랭크명령어 멘션으로 경고바랍니다."%message.author.id, allowed_mentions = discord.AllowedMentions.none())
            return True
    mxlen = dc[message.guild].maxmsglen
    if len(message.content) > mxlen:
        await message.channel.send("<@%d> %d자 초과로 삭제되었습니다."%(message.author.id, mxlen), delete_after = 1.0)
        return True
    if message.content.count('\n') > 4:
        await message.channel.send("<@%d> 5줄 이상은 안받아요."%message.author.id, delete_after = 1.0)
        return True
    return False

async def autoreact(message):
    rmdc = dc[message.guild].reaction_macro
    if message.author in rmdc:
        await message.add_reaction(rmdc[message.author])

async def attach_mdr(message):
    global dc, imgdc
    ofls, cfls = [], []
    cnt = 0
    for att in message.attachments:
        opth = 'ats/' + att.filename
        await att.save(opth)
        ofl = discord.File(open(opth, 'rb'))
        ofls.append(ofl)
        npth = imagecomp.comp(opth)
        if opth == npth: cfls.append(ofl)
        else:
            cfls.append(discord.File(open(npth, 'rb')))
            cnt += 1
    cnl = dc[message.guild].cnls.attachlog
    if len(ofls) and cnl != None:
        dispname = message.author.nick
        if dispname == None: dispname = message.author.name
        await cnl.send(content = '<@%d> >> %s'%(message.author.id, message.content), files = ofls,
            allowed_mentions=discord.AllowedMentions.none())
        if cnt:
            await message.delete()
            msg = await message.channel.send(content = '%s >> %s'%(dispname, message.content), files = cfls,
                allowed_mentions=discord.AllowedMentions.none())
            await msg.add_reaction('❌')
            imgdc[msg] = message.author.id

class Core(commands.Cog):
    def __init__(self, app):
        self.app = app

    @commands.Cog.listener()
    async def on_message(self, message):
        global dc
        if message.author.bot: return
        gld = message.guild
        if gld not in dc: dc[gld] = GuildData()
        if await filter_message(message):
            await message.delete()
            return
        await autoreact(message)
        if len(message.attachments): await attach_mdr(message)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        global dc, imgdc
        if user.bot: return
        if reaction.message in imgdc and reaction.emoji == '❌':
            if user.id == imgdc[reaction.message]:
                del imgdc[reaction.message]
                await reaction.message.delete()
                return
        if user.top_role.name in ["서버장", "대장"]: return
        msg = reaction.message
        cnl = msg.channel
        gld = msg.guild
        if gld not in dc: dc[gld] = GuildData()
        if cnl in dc[gld].cnls.ignore: return
        if reaction.emoji == '🖕':
            await reaction.clear()
            await middle_finger_report(gld, user.id, cnl)

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        global dc
        if user.bot: return
        gld = reaction.message.guild
        if gld not in dc: dc[gld] = GuildData()
        if reaction.message.channel in dc[gld].cnls.ignore: return
        ec = dc[gld].cnls.emojilog
        if ec != None:
            embed = discord.Embed(description='From %s, <@%d> removed this emoji ⬇'%(reaction.message.jump_url, user.id))
            msg = await ec.send(embed=embed)
            await msg.add_reaction(reaction)
