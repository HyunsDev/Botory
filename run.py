import asyncio, discord
from discord.ext import commands
import cmds, mdrs

app = commands.Bot(command_prefix='bt!', intents=discord.Intents.all())

if __name__ == "__main__":
    testtoken = 'NzkyMjg2ODU2ODI5ODYxODk4.X-bgog.aQ06fxs9SfGQRngOSGTuMpv1qXE'
    token = 'Nzc1NjA2OTc3NzEwNzg0NTM0.X6oySQ.uVjDhkMJrHRAIGDYEQIM5Pc6F68'
    app.add_cog(cmds.Core(app))
    app.add_cog(mdrs.Core(app))
    app.run(testtoken)
