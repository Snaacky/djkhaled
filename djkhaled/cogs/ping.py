import logging
from discord.ext import commands


class PingCog(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def ping(self, ctx: commands.Context) -> None:
        latency = round(self.bot.latency * 1000)
        await ctx.send(f"Pong! Latency is ~{latency}ms.")


async def setup(bot) -> None:
    await bot.add_cog(PingCog(bot))
    logging.info("Cog loaded: ping")
