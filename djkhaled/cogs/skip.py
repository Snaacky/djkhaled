import discord
from discord.ext import commands

from djkhaled.embeds import send_embed, send_error
from djkhaled.state import voice_clients
from djkhaled.utils import after_song


class Skip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="skip")
    async def skip(self, ctx: commands.Context):
        """
        Skip the current playing audio without disconnecting from the voice channel.
        """
        client = voice_clients[ctx.guild.id]
        if not client:
            return await send_error(ctx, "No audio is currently playing.")

        client.stop()
        await send_embed(ctx, "⏭️ Skipped", "Skipped the current track.", discord.Color.green())
        await after_song(ctx)


async def setup(bot):
    await bot.add_cog(Skip(bot))
    print("Cog loaded: skip")
