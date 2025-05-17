import asyncio
import logging

import discord
from discord.ext import commands

from djkhaled.config import config
from djkhaled.state import GuildState, state


logging.basicConfig(level=logging.DEBUG)


# TODO: Does thie even work? Do we need to write different code for debugging?
class DJKhaledBot(commands.Bot):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        async def close(self) -> None:
            # TODO: on bot shutdown, disconnect from voice channels
            for guild in state.items():
                logging.info(guild)

            await super().close()


bot = DJKhaledBot(
    activity=discord.Game(name=f"music, use {config.discord.prefix}play"),
    command_prefix=config.discord.prefix,
    intents=discord.Intents.all(),
)


@bot.event
async def on_ready() -> None:
    logging.info(f"Logged in as: {bot.user}")
    for guild in bot.guilds:
        state[guild.id] = GuildState()


# TODO: on new server join event, populate state


@bot.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState) -> None:
    """Event listener for voice state changes. Clears state when bot disconnects from voice channel."""
    if member == bot.user and before.channel and not after.channel:
        gstate = state[before.channel.guild.id]
        gstate.playing = None
        gstate.client = None
        gstate.queue.clear()


@bot.event
async def on_message(message: discord.Message) -> None:
    if message.author == bot.user:
        return

    logging.info(f"Message from {message.author}: {message.content}")
    await bot.process_commands(message)


async def main() -> None:
    try:
        await bot.load_extension("djkhaled.cogs.debug")
        await bot.load_extension("djkhaled.cogs.ping")
        await bot.load_extension("djkhaled.cogs.play")
        await bot.load_extension("djkhaled.cogs.queue")
        await bot.load_extension("djkhaled.cogs.remove")
        await bot.load_extension("djkhaled.cogs.seek")
        await bot.load_extension("djkhaled.cogs.skip")
        await bot.load_extension("djkhaled.cogs.stop")
    except Exception as e:
        logging.error(f"Error loading extension: {e}")

    await bot.start(config.discord.token)


if __name__ == "__main__":
    asyncio.run(main())
