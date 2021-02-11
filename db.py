import asyncio, pickle, os
import discord

botversion = '1.6.1'
adroles = ['경찰', '검찰', '의원']
cnlnames = ['report', 'rankonly', 'emojilog', 'attachlog']

class GuildDatum:
    def __init__(self):
        self.guild = None
        self.cnls = dict()
        for cnlname in cnlnames: self.cnls[cnlname] = None
        self.igcnls = []
        self.autoreacts = dict()
        self.maxmsglen = 200
        self.banishdata = dict()
    def _export(self):
        ret = dict()
        ret['cnls'] = []
        for cnlname in self.cnls:
            if self.cnls[cnlname] != None: ret['cnls'].append(self.cnls[cnlname].id)
            else: ret['cnls'].append(None)
        ret['icnls'] = []
        for cnl in self.igcnls: ret['icnls'].append(cnl.id)
        ret['ars'] = dict()
        for who in self.autoreacts: ret['ars'][who.id] = self.autoreacts[who]
        ret['mml'] = self.maxmsglen
        ret['bd'] = dict()
        for who in self.banishdata:
            sbd = self.banishdata[who]
            onick = sbd[0]
            orls = []
            for rl in sbd[1]: orls.append(rl.id)
            ret['bd'][who.id] = (onick, orls)
        return ret
    def _import(self, _db, app):
        self.guild = app.guilds[0]
        self.cnls = dict()
        for i in range(len(cnlnames)):
            self.cnls[cnlnames[i]] = discord.utils.get(self.guild.channels, id = _db['cnls'][i])
        self.icnls = []
        for cnlid in _db['icnls']:
            self.icnls.append(discord.utils.get(self.guild.channels, id = cnlid))
        self.autoreacts = dict()
        for whoid in _db['ars']:
            who = discord.utils.get(self.guild.members, id = whoid)
            self.autoreacts[who] = _db['ars'][whoid]
        self.maxmsglen = _db['mml']
        self.banishdata = dict()
        for whoid in _db['bd']:
            who = discord.utils.get(self.guild.members, id = whoid)
            onick = _db['bd'][whoid][0]
            orls = []
            for rlid in _db['bd'][whoid][1]:
                rl = discord.utils.get(self.guild.roles, id = rlid)
                orls.append(rl)
            self.banishdata[who] = (onick, orls)

db = GuildDatum()
imgdc = dict()

def m2m(who, gld):
    who = who[2:-1]
    if who[0] == '!': who = who[1:]
    who = discord.utils.get(gld.members, id = int(who))
    return who

def savedb():
    global db
    print('Data saving...')
    _db = db._export()
    with open('db.pkl', 'wb') as f:
        pickle.dump(_db, f, protocol=pickle.HIGHEST_PROTOCOL)
    print('Data saved!')

def loaddb(app):
    global db
    print('Data loading...')
    if not os.path.isfile('db.pkl'):
        print('No data loaded')
        return
    with open('db.pkl', 'rb') as f:
        _db = pickle.load(f)
    db._import(_db, app)
    print('Data loaded!')
