from discord.ext import commands
import discord
import sqlite3
from utils.database import SongPlaysDatabase


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def setup(self, bot):
        self.db = sqlite3.connect('database.db')  # Connect to the database here
        bot.add_cog(General(bot))

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Logged in as {self.bot.user} (ID: {self.bot.user.id})")
    @commands.command(help="Shows how many songs a user has played.")
    async def getplays(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        plays = self.db.get_plays(user.id)
        await ctx.send(f"{user.display_name} has played {plays} songs.")

    @commands.command(help="Lists play counts for all users.")
    async def listplays(self, ctx):
        plays_list = self.db.list_all_plays()
        if plays_list:
            embed = discord.Embed(title="Play Counts", color=discord.Color.blue())
            for user_id, plays in plays_list:
                user = self.bot.get_user(user_id) or user_id
                embed.add_field(name=f"{user}", value=f"Plays: {plays}", inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send("No play data found.")

    @commands.command(name='help', help="Shows help information for commands.")
    async def help_command(self, ctx, *, command: str = None):
        if command is None:
            embed = discord.Embed(title="Help", color=discord.Color.purple(), description="List of available commands:")
            for cmd in self.bot.commands:
                if not cmd.hidden and cmd.name != 'help':
                    embed.add_field(name=f"!{cmd.name}", value=cmd.help, inline=False)
            await ctx.send(embed=embed)
        else:
            cmd = self.bot.get_command(command)
            if cmd:
                embed = discord.Embed(title=f"!{cmd.name}", description=cmd.help or "No description available.",
                                      color=discord.Color.green())
                await ctx.send(embed=embed)
            else:
                await ctx.send("Command not found.")


def setup(bot):
    db = SongPlaysDatabase()
    bot.add_cog(General(bot, db))
