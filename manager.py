from multiprocessing import managers
from discord.ext import commands
from discord.ext.commands.errors import MissingRequiredArgument, CommandError

class Manager(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Estou conectado como {self.bot.user}')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, MissingRequiredArgument):
            ctx.send('Tem um argumuainto falteido')
        elif isinstance(error, CommandError):
            ctx.send('Esse comeindo nau é existeido')


def setup(bot):
    bot.add_cog(Manager(bot))