import logging

import discord
from discord.ext import commands

from djkhaled.embeds import send_embed, send_error
from djkhaled.state import state
from djkhaled.utils import after_song


class Skip(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(name="skip")
    @commands.guild_only()
    async def skip(self, ctx: commands.Context) -> None:
        """
        Skip the current playing audio without disconnecting from the voice channel.
        """
        gstate = state[ctx.guild.id]

        if not gstate.client:
            return await send_error(ctx, "No audio is currently playing.")

        gstate.client.stop()
        await send_embed(ctx, "⏭️ Skipped", "Skipped the current track.", discord.Color.green())
        await after_song(ctx)


async def setup(bot) -> None:
    await bot.add_cog(Skip(bot))
    logging.info("Cog loaded: skip")
