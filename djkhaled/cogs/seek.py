import discord
from discord.ext import commands

from djkhaled.embeds import send_embed, send_error
from djkhaled.state import voice_clients
from djkhaled.utils import stream_audio


class Seek(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="seek")
    async def seek(self, ctx: commands.Context, time: int):
        """
        Seek to a specific time in the current audio.
        """
        client = voice_clients[ctx.guild.id]

        if not client or not client.is_playing():
            return await send_error(ctx, "No audio is currently playing.")

        client = voice_clients[ctx.guild.id]
        client.stop()

        # TODO: This definitely doesn't work right now because I removed the time parameter...
        # TODO: Also what the fuck is going on with that message content split?
        # await stream_audio(ctx=ctx, ctx.message.content.split(" ")[1], time)
        await send_embed(ctx, "✅ Seeked", f"Jumped to {time} seconds in the audio.", discord.Color.green())


async def setup(bot):
    await bot.add_cog(Seek(bot))
    print("Cog loaded: seek")
