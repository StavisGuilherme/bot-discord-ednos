from discord.ext import commands
import discord
import asyncio


class Talks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        

    @commands.command(name='artuaista')
    async def artuaista(self, ctx):
        emojis = ['👍', '👎']
        message = await ctx.send(f'Você é artuaista, {ctx.author.name}?')
        for emoji in emojis:
            await message.add_reaction(emoji)

        def check(reaction, union):
            return union.id == ctx.author.id and reaction.message.channel.id == ctx.channel.id and str(reaction.emoji) in emojis
        try:
            reaction, user = await self.bot.wait_for(event='reaction_add', timeout=10, check=check)

            if reaction.emoji == emojis[0]:
                await ctx.send('É MENTUAIRA')
            elif reaction.emoji == emojis[1]:
                await ctx.send('Eu sabuaia')
        except asyncio.TimeoutError:
            await message.edit(content=message.content +'\n\n*Esse comando já expirou*')

    @commands.command(name='mateire')
    async def mateire(self, ctx):
        channel = ctx.message.author.voice.channel
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
        
        voice.play(discord.FFmpegPCMAudio('vai-me-mateire.mp3'))
        #await voice.disconnect()

    #@commands.command(name='leave')
    #async def leave(self, ctx):
    #    voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
    #    if voice and voice.is_connected():
    #        await voice.disconnect()        

def setup(bot):
    bot.add_cog(Talks(bot))