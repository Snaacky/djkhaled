import asyncio

import discord
from discord.ext import commands

from djkhaled.config import config

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())


@bot.event
async def on_ready() -> None:
    print(f"Logged in as: {bot.user.username}")


@bot.event
async def on_message(message):
    print(f"Message from {message.author}: {message.content}")

    if message.author == bot.user:
        return

    await bot.process_commands(message)


async def main():
    try:
        await bot.load_extension("djkhaled.cogs.ping")
        await bot.load_extension("djkhaled.cogs.streaming")
    except Exception as e:
        print(f"Error loading extension: {e}")
        raise e
    await bot.start(config.discord.bot_token)


if __name__ == "__main__":
    asyncio.run(main())
