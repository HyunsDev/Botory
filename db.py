# -*- coding:cp949 -*-

import discord
dc = dict()
class GuildData:
    class ChannelsData:
        def __init__(self):
            self.report = self.rankonly = self.emojilog = None
            self.ignore = []
        def __getitem__(self, key):
            if key == 'report': return self.report
            elif key == 'rankonly': return self.rankonly
            elif key == 'emojilog': return self.emojilog
            elif key == 'ignore': return self.ignore
            else: raise KeyError
        def __setitem__(self, key, value):
            if key == 'report': self.report = value
            elif key == 'rankonly': self.rankonly = value
            elif key == 'emojilog': self.emojilog = value
            elif key == 'ignore': self.ignore = value
            else: raise KeyError
    def __init__(self):
        self.cnls = self.ChannelsData()
        self.reaction_macro = dict()
        self.maxmsglen = 200
        self.banishdata = dict()
