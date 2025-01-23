import discord
from discord.ext import commands

from djkhaled.embeds import send_embed
from djkhaled.state import voice_clients


class Stop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="stop")
    async def stop(self, ctx: commands.Context):
        """
        Stop the currently playing audio and disconnect.
        """
        client = voice_clients[ctx.guild.id]
        if client:
            await client.stop()
            return await send_embed(ctx, "✅ Stopped", "Disconnected from the voice channel.", discord.Color.green())

        return await send_embed(ctx, "❌ Error", "I am not connected to a voice channel.", discord.Color.red())


async def setup(bot):
    await bot.add_cog(Stop(bot))
    print("Cog loaded: stop")
