import logging

import discord
from discord.ext import commands
from pytimeparse import parse

from djkhaled.embeds import send_embed, send_error
from djkhaled.state import state
from djkhaled.utils import stream_audio


class Seek(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(name="seek")
    @commands.guild_only()
    async def seek(self, ctx: commands.Context, time: str) -> None:
        """
        Seek to a specific time in the current audio.
        """
        # TODO: 99% sure this breaks if there is a queue
        # TODO: Make sure that we can't see before or after the song length
        # TODO: Would be nice if we didn't need to re-ytldp the song once we already have the data...
        gstate = state[ctx.guild.id]

        if not gstate.client or not gstate.client.is_playing() or not gstate.playing:
            return await send_error(ctx, "No audio is currently playing.")

        gstate.client.stop()
        await stream_audio(ctx=ctx, track=gstate.playing, skip_to=parse(time))
        await send_embed(ctx, "✅ Seeked", f"Jumped to {time} in the current playing audio.", discord.Color.green())


async def setup(bot) -> None:
    await bot.add_cog(Seek(bot))
    logging.info("Cog loaded: seek")
