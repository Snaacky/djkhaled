import logging

import discord
from discord.ext import commands

from djkhaled.embeds import send_embed, send_error
from djkhaled.state import state


class Remove(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(name="remove")
    @commands.guild_only()
    async def remove(self, ctx: commands.Context, index: int) -> None:
        """
        Remove a song from the queue by its ID/index.
        """
        gstate = state[ctx.guild.id]

        if index < 1 or index > len(gstate.queue):
            return await send_error(ctx, "Invalid song index. Please provide a valid index from the queue.")

        song = gstate.queue.pop(index - 1)

        await send_embed(
            ctx,
            "✅ Removed from Queue",
            f"Removed **{song.url}** from the queue.",
            discord.Color.green(),
        )


async def setup(bot) -> None:
    await bot.add_cog(Remove(bot))
    logging.info("Cog loaded: remove")
