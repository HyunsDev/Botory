import os, pickle
from discord.ext import commands

class DBCog(commands.Cog):
    def __init__(self, app):
        self.app = app
        self.DB = dict()
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
        member_id = who[2:-1]
        if member_id[0] == '!': member_id = member_id[1:]
        member_id = int(member_id)
        return guild.get_member(member_id)
