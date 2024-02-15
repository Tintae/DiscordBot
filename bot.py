from discord.ext import commands
from utils.settings import TOKEN, intents


async def main():
    # Create the bot instance
    bot = commands.Bot(command_prefix='!', intents=intents)

    # Correctly load extensions without awaiting
    await bot.load_extension("cogs.music")
    await bot.load_extension("cogs.general")

    # Start the bot with the token from settings.py
    await bot.start(TOKEN)  # This should be awaited because bot.start is a coroutine

    # This will only run if the bot is stopped with CTRL+C or SIGINT
    print("Shutting down...")
    await bot.close()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())  # Correct usage of asyncio.run for Python 3.10 and newer
