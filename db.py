import discord

adroles = ['경찰', '검찰', '의원']
dc = dict()
class GuildData:
    class ChannelsData:
        def __init__(self):
            self.report = self.rankonly = self.emojilog = self.attachlog = None
            self.ignore = []
        def __getitem__(self, key):
            if key == 'report': return self.report
            elif key == 'rankonly': return self.rankonly
            elif key == 'emojilog': return self.emojilog
            elif key == 'ignore': return self.ignore
            elif key == 'attachlog': return self.attachlog
            else: raise KeyError
        def __setitem__(self, key, value):
            if key == 'report': self.report = value
            elif key == 'rankonly': self.rankonly = value
            elif key == 'emojilog': self.emojilog = value
            elif key == 'ignore': self.ignore = value
            elif key == 'attachlog': self.attachlog = value
            else: raise KeyError
    def __init__(self):
        self.cnls = self.ChannelsData()
        self.reaction_macro = dict()
        self.maxmsglen = 200
        self.banishdata = dict()

def m2m(who, gld):
    who = who[2:-1]
    if who[0] == '!': who = who[1:]
    who = discord.utils.get(gld.members, id = int(who))
    return who
