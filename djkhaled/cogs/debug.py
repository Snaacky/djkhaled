import logging

import discord
from discord.ext import commands

from djkhaled.config import config
from djkhaled.embeds import send_embed
from djkhaled.state import state


class DebugCog(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def debug(self, ctx: commands.Context) -> None:
        if ctx.author.id in config.djkhaled.admins:
            await ctx.send(state[ctx.guild.id])
        else:
            return await send_embed(
                ctx,
                "❌ Error",
                "You are not listed as an admin in the config!",
                discord.Color.red(),
            )


async def setup(bot) -> None:
    await bot.add_cog(DebugCog(bot))
    logging.info("Cog loaded: debug")
