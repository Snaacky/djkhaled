import logging

import discord
from discord.ext import commands

from djkhaled.embeds import send_error
from djkhaled.state import state


class Queue(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(name="queue")
    @commands.guild_only()
    async def queue(self, ctx: commands.Context) -> None:
        """
        Command to show the current song queue.
        """
        # todo: command must be ran in guild
        gstate = state[ctx.guild.id]

        if not gstate.client:
            return await send_error(ctx, "No audio is currently playing.")

        if not gstate.queue:
            return await send_error(ctx, "There are no songs currently in queue.")

        embed = discord.Embed(
            title="🎶 Current Song Queue",
            description="Here are the songs in the queue:\n",
            color=discord.Color.blue(),
        )

        for index, song in enumerate(gstate.queue, start=1):
            embed.description += f"**{index}.** {song.url} (Requested by: {song.requester.name})\n"

        await ctx.send(embed=embed)


async def setup(bot) -> None:
    await bot.add_cog(Queue(bot))
    logging.info("Cog loaded: queue")
