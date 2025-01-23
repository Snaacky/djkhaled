import discord
from discord.ext import commands

from djkhaled.embeds import send_error
from djkhaled.state import song_queue, voice_clients


class Queue(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="queue")
    async def queue(self, ctx: commands.Context):
        """
        Command to show the current song queue.
        """
        client = voice_clients[ctx.guild.id]
        _queue = song_queue[ctx.guild.id]

        if not client:
            return await send_error(ctx, "No audio is currently playing.")

        if not _queue:
            return await send_error(ctx, "There are no songs currently in queue.")

        embed = discord.Embed(
            title="🎶 Current Song Queue",
            description="Here are the songs in the queue:\n",
            color=discord.Color.blue(),
        )

        for index, song in enumerate(_queue, start=1):
            embed.description += f"**{index}.** {song['url']} (Requested by: {song['requester'].name})\n"

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Queue(bot))
    print("Cog loaded: queue")
