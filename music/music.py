
import discord
from discord.ext import commands
from youtube_dl import YoutubeDL

class Music(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

        self.is_playing = False
        self.is_paused = False

        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        self.vc = None

    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info('ytsearch:%s' % item, download=False)['entries'][0]
            except Exception:
                return False

        return {'source': info['formats'][0]['url'], 'title': info['title']}

    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']

            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    async def play_music(self, ctx):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']

            if self.vc == None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()

                if self.vc == None:
                    await ctx.send('Nao deu pra conectar no voice')
                    return

            else:
                await self.vc.move_to(self.music_queue[0][1])

            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False


    @commands.command(name='play', aliases=['p'])
    async def play(self, ctx, *args):
        query = ' '.join(args)

        voice_channel = ctx.author.voice.channel

        if voice_channel is None:
            await ctx.send('nao ta em lugar nenhum corno')

        elif self.is_paused:
            self.vc.resume()
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send("Could not download the song. Incorrect format try another keyword. This could be due to playlist or a livestream format.")
            else:
                await ctx.send('deu boa, adicionou no cu')
                self.music_queue.append([song, voice_channel])

                if self.is_playing == False:
                    await self.play_music(ctx)

    

    @commands.command(name='pause')
    async def pause(self, ctx, *args):
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
        elif self.is_paused:
            self.vc.resume()

    @commands.command(name='resume', aliases=['r'])
    async def resume(self, ctx, *args):
        if self.is_paused:
            self.vc.resume()

    @commands.command(name='skip', aliases=['s'])
    async def skip(self, ctx):
        if self.vc != None and self.vc:
            self.vc.stop()
            await self.play_music(ctx)

    @commands.command(name='queue', aliases=['q'])
    async def queue(self, ctx):
        retval = ''

        for i in range(0, len(self.music_queue)):
            if i > 4: break
            retval += self.music_queue[i][0]['title'] + '\n' 

        if retval != '':
            await ctx.send(retval)
        else:
            await ctx.send('cabo corno')

    @commands.command(name='clear', aliases=['c'])
    async def clear(self, ctx):
        if self.vc != None and self.is_playing:
            self.vc.stop()
        self.music_queue = []
        await ctx.send('limpou')

    @commands.command(name='leave', aliases=['l'])
    async def leave(self, ctx):
        self.is_paused = False
        self.is_playing = False
        await self.vc.disconnect()


    #@commands.command(name='play')
    #async def play(self, ctx, url):

        #loop = asyncio.get_event_loop()
        #data = await loop.run_in_executor(None, lambda: self.ytdl.extract_info(url, download=not True))

        #if 'entries' in data:
        #    data = data['entries'][0]

        #filename = data['url']
        #print(filename)


        #channel = ctx.message.author.voice.channel
        #voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

        #if voice and voice.is_connected():
        #    await voice.move_to(channel)
        #else:
        #    voice = await channel.connect()

        #player = discord.FFmpegPCMAudio(filename, **ffmpeg_options)
        #try:
        #    ctx.voice_client.play(player)
        #except ClientException:
        #    await ctx.send('Espera ai porra')



def setup(bot):
    bot.add_cog(Music(bot))
