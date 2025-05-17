import logging
import traceback

import discord
from discord.ext import commands

from djkhaled.embeds import send_embed, send_error
from djkhaled.state import state, Track
from djkhaled.utils import stream_audio


class Play(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(name="play")
    @commands.guild_only()
    async def play(self, ctx: commands.Context, url: str) -> None:
        """
        Command to play a URL in a voice channel.
        """
        # TODO: Add support for ytsearch

        if not ctx.author.voice or ctx.author.voice.channel.guild.id != ctx.guild.id:
            return await send_error(ctx, "You need to join a voice channel in this server first.")

        gstate = state[ctx.guild.id]
        channel = ctx.author.voice.channel
        track = Track(url=url, requester=ctx.author)

        # Add to the current queue if the a voice client object already exists.
        if gstate.client and gstate.client.is_playing():
            gstate.queue.append(track)
            return await send_embed(
                ctx,
                "✅ Added to Queue",
                f"Added to the queue. There are {len(gstate.queue)} songs in the queue.",
                discord.Color.green(),
            )

        # Verify the bot can connect to the channel and create a new voice client object.
        if not gstate.client or (gstate.client and not gstate.client.is_connected()):
            permissions = channel.permissions_for(ctx.guild.me)
            if not permissions.view_channel:
                return await send_error(ctx, "I do not have permission to view that voice channel.")
            if not permissions.connect:
                return await send_error(ctx, "I do not have permission to connect to that voice channel.")
            if not permissions.speak:
                return await send_error(ctx, "I do not have permission to speak in that voice channel.")

            gstate.client = await channel.connect(self_deaf=True)

        # Once the bot is connected to the channel, begin streaming the audio.
        try:
            await stream_audio(ctx=ctx, track=track)
        except Exception:
            await send_error(ctx, "An error occurred while attempting to stream audio, check console for details.")
            logging.error(traceback.format_exc())


async def setup(bot) -> None:
    await bot.add_cog(Play(bot))
    logging.info("Cog loaded: play")
