from discord.ext import commands
from utils.settings import TOKEN, intents
import discord
import nacl
async def setup_bot():
    # Create the bot instance
    bot = commands.Bot(command_prefix='!', intents=discord.Intents.all(), help_command=None)

    # Define the on_command_error event handler inside the setup function
    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("Sorry, I can't find that command. 😕")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have the required permissions to run this command.")
        else:
            await ctx.send("Oops! Something went wrong while executing the command.")
            # Log the error for debugging purposes
            print(f"Error executing command: {type(error).__name__}: {error}")

    # Load extensions
    await bot.load_extension("cogs.music")
    await bot.load_extension("cogs.general")

    # Start the bot with the token from settings.py
    await bot.start(TOKEN)

if __name__ == "__main__":
    import asyncio
    asyncio.run(setup_bot())  # Correct usage of asyncio.run for Python 3.10 and newer
