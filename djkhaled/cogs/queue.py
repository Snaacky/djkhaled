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

        if not client or not client.is_playing():
            return await send_error(ctx, "No audio is currently playing.")

        embed = discord.Embed(
            title="🎶 Current Song Queue",
            description="Here are the songs in the queue:",
            color=discord.Color.blue(),
        )

        if _queue:
            current_song = _queue[0]
            embed.add_field(
                name="Now Playing",
                value=f"**{current_song['url']}** (Requested by: {current_song['requester'].name})",
                inline=False,
            )

        for index, song in enumerate(_queue[1:], start=2):
            song_info = f"**{index}.** {song['url']} (Requested by: {song['requester'].name})"
            embed.add_field(name=f"Song {index}", value=song_info, inline=False)

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Queue(bot))
    print("Cog loaded: queue")
