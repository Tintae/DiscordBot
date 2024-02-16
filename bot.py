from discord.ext import commands
from utils.settings import TOKEN
import discord
import nacl
import logging

# Configure logging
logging.basicConfig(filename='bot_activity.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

async def setup_bot():
    # Define specific intents for the bot
    intents = discord.Intents.default()
    intents.members = True
    intents.typing = True
    intents.presences = True
    intents.message_content = True

    # Create the bot instance with the specified intents
    bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

    # Event Handlers (moved outside of setup_bot)
    @bot.event
    async def on_ready(self):  # 'self' is now included
        logging.info(f"Logged in as {self.user} (ID: {self.user.id})")
    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("Sorry, I can't find that command. 😕")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have the required permissions to run this command.")
        else:
            await ctx.send("Oops! Something went wrong while executing the command.")
            logging.error(f"Error executing command: {type(error).__name__}: {error}")

    # Load extensions
    await bot.load_extension("cogs.music")
    await bot.load_extension("cogs.general")

    await bot.start(TOKEN)


if __name__ == "__main__":
    import asyncio

    asyncio.run(setup_bot())
