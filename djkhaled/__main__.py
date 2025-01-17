import asyncio

import discord
from discord.ext import commands

from djkhaled.config import config

bot = commands.Bot(
    activity=discord.Game(name=f"music, use {config.discord.prefix}play"),
    command_prefix=config.discord.prefix,
    intents=discord.Intents.all(),
)


@bot.event
async def on_ready() -> None:
    print(f"Logged in as: {bot.user}")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    print(f"Message from {message.author}: {message.content}")

    await bot.process_commands(message)


async def main():
    try:
        await bot.load_extension("djkhaled.cogs.ping")
        await bot.load_extension("djkhaled.cogs.play")
        await bot.load_extension("djkhaled.cogs.queue")
        await bot.load_extension("djkhaled.cogs.remove")
        await bot.load_extension("djkhaled.cogs.seek")
        await bot.load_extension("djkhaled.cogs.skip")
        await bot.load_extension("djkhaled.cogs.stop")
    except Exception as e:
        print(f"Error loading extension: {e}")

    await bot.start(config.discord.token)


if __name__ == "__main__":
    asyncio.run(main())
