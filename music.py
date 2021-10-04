import discord
from discord.ext import commands
import youtube_dl
import asyncio

# create queuelist
queueList = []

class music(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def play_song(self,ctx):
      def after_song(kool):
        queueList.pop(0)
        #pop song from the list once it has been played
        
      while True:
        # if bot is already playing music, sleep this, else play next song
        if ctx.voice_client.is_playing() or ctx.voice_client.is_paused():
          await asyncio.sleep(1)
        else:
          await ctx.channel.send(f'currently playing {queueList[0]}')
          url = queueList[0]
          FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
          YDL_OPTIONS = {'format':"bestaudio"}
          vc = ctx.voice_client

          with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
            vc.play(source, after=after_song)
            continue
  
    
    @commands.command()
    async def join(self,ctx):
        if ctx.author.voice is None:
            await ctx.send("you arent in a voice channel")
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)

    @commands.command()
    async def leave(self,ctx):
        await ctx.voice_client.disconnect()
        await ctx.channel.send("byeeee")

    @commands.command()
    async def play(self,ctx):
      if queueList == []:
        await ctx.channel.send('no songs in queue, use $queue command to add songs')
      else:
        ctx.voice_client.stop()
        # play song using play_song command
        await self.play_song(ctx)
        await ctx.channel.send("playing the song")
          
    
    @commands.command()
    async def queue(self,ctx,url):
      queueList.append(url)


    @commands.command()
    async def pause(self,ctx):
        ctx.voice_client.pause()
        await ctx.channel.send("paused the song")
    
    @commands.command()
    async def resume(self,ctx):
        ctx.voice_client.resume()
        await ctx.channel.send("resuming!")

def setup(client):
    client.add_cog(music(client))
