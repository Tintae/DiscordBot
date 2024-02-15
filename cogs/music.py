from discord.ext import commands
import discord
import yt_dlp
from utils.settings import ydl_opts
from utils.database import SongPlaysDatabase

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = SongPlaysDatabase()

    def check_queue(self, ctx, server_id):
        if self.queues.get(server_id):
            source = self.queues[server_id].pop(0)
            ctx.voice_client.play(source, after=lambda x=None: self.check_queue(ctx, server_id))

    @commands.command(help="Joins the author's voice channel.")
    async def join(self, ctx):
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            await channel.connect()
            await ctx.send(f"🔊 Joined `{channel.name}`.")
        else:
            await ctx.send("🚫 You are not in a voice channel.")

    @commands.command(help="Leaves the current voice channel.")
    async def leave(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("🔇 Left the voice channel.")
        else:
            await ctx.send("🚫 I'm not in any voice channel.")

    @commands.command(help="Plays a song from YouTube based on a search query or URL.")
    async def play(self, ctx, *, query: str):
        if not ctx.author.voice or not ctx.author.voice.channel:
            await ctx.send("🚫 You need to be in a voice channel to play music.")
            return

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=False)
            url = info['entries'][0]['formats'][0]['url']
            title = info['entries'][0]['title']

        if not ctx.voice_client.is_playing():
            source = discord.FFmpegPCMAudio(url)
            ctx.guild.voice_client.play(source, after=lambda x=None: self.check_queue(ctx, ctx.guild.id))
            await ctx.send(f"🎵 Now playing: **{title}**")
            self.db.increment_plays(ctx.author.id)
        else:
            server_id = ctx.guild.id
            if server_id not in self.queues:
                self.queues[server_id] = []
            self.queues[server_id].append(discord.FFmpegPCMAudio(url))
            await ctx.send(f"🎵 **{title}** added to the queue.")

    @commands.command(name='queue', help='Shows the current music queue.')
    async def show_queue(self, ctx):
        server_id = ctx.guild.id
        if server_id in self.queues and self.queues[server_id]:
            queue_embed = discord.Embed(title="Music Queue", description="", color=discord.Color.blue())
            for i, source in enumerate(self.queues[server_id], start=1):
                queue_embed.description += f"{i}. Song {i}\n"
            await ctx.send(embed=queue_embed)
        else:
            await ctx.send("The queue is currently empty.")

def setup(bot):
    bot.add_cog(Music(bot))
