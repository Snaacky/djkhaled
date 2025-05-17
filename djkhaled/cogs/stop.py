import logging

import discord
from discord.ext import commands

from djkhaled.embeds import send_embed
from djkhaled.state import state


class Stop(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(name="stop")
    @commands.guild_only()
    async def stop(self, ctx: commands.Context) -> None:
        """
        Stop the currently playing audio and disconnect.
        """
        gstate = state[ctx.guild.id]

        if not gstate.client:
            return await send_embed(ctx, "❌ Error", "I am not connected to a voice channel.", discord.Color.red())

        await gstate.client.stop()
        return await send_embed(ctx, "✅ Stopped", "Disconnected from the voice channel.", discord.Color.green())


async def setup(bot) -> None:
    await bot.add_cog(Stop(bot))
    logging.info("Cog loaded: stop")
