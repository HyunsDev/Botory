import asyncio, discord, sys, os
import pickle
import db
from discord.ext import commands
import cmds, mdrs, stats

app = commands.Bot(command_prefix='bt!', intents=discord.Intents.all())

@app.event
async def on_ready():
    await app.change_presence(activity = discord.Game('Botory %s by Undec'%db.botversion))
    db.loaddb(app)

if __name__ == "__main__":
    if not os.path.isfile('tokens.pkl'):
        tt = input('testtoken :')
        rt = input('realtoken :')
        with open('tokens.pkl', 'wb') as f: pickle.dump((tt, rt), f)
    with open('tokens.pkl', 'rb') as f: tt, rt = pickle.load(f)
    if not os.path.exists('ats'): os.makedirs('ats')
    app.add_cog(cmds.Core(app))
    app.add_cog(mdrs.Core(app))
    app.add_cog(stats.Core(app))
    if len(sys.argv) < 2: app.run(tt)
    elif sys.argv[1] != 'realwork': app.run(tt)
    else: app.run(rt)
    db.savedb()
