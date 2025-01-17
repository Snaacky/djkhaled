import discord
from discord.ext import commands

from djkhaled.embeds import send_embed, send_error
from djkhaled.state import song_queue


class Remove(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="remove")
    async def remove(self, ctx: commands.Context, index: int):
        """
        Remove a song from the queue by its ID/index.
        """
        queue = song_queue[ctx.guild.id]

        if index < 1 or index > len(queue):
            return await send_error(ctx, "Invalid song index. Please provide a valid index from the queue.")

        song = queue.pop(index - 1)

        await send_embed(
            ctx,
            "✅ Removed from Queue",
            f"Removed **{song['url']}** from the queue.",
            discord.Color.green(),
        )


async def setup(bot):
    await bot.add_cog(Remove(bot))
    print("Cog loaded: remove")
