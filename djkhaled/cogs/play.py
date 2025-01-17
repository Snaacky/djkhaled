import traceback

import discord
from discord.ext import commands
from yt_dlp.utils import DownloadError

from djkhaled.embeds import send_embed, send_error
from djkhaled.state import song_queue, voice_clients
from djkhaled.utils import stream_audio


class Play(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="play")
    async def play(self, ctx: commands.Context, url: str):
        """
        Command to play a URL in a voice channel.
        """
        if not ctx.author.voice:
            return await send_error(ctx, "You need to join a voice channel first.")

        client = voice_clients.get(ctx.guild.id)
        channel = ctx.author.voice.channel
        queue = song_queue.get(ctx.guild.id)

        if not client:
            permissions = channel.permissions_for(ctx.guild.me)
            if not permissions.view_channel:
                return await send_error(ctx, "I do not have permission to view that voice channel.")
            if not permissions.connect:
                return await send_error(ctx, "I do not have permission to connect to that voice channel.")
            if not permissions.speak:
                return await send_error(ctx, "I do not have permission to speak in that voice channel.")

            client = await channel.connect()
            voice_clients[ctx.guild.id] = client

        if client and client.is_playing():
            queue.append({"url": url, "requester": ctx.author})
            return await send_embed(
                ctx,
                "✅ Added to Queue",
                f"Added to the queue. There are {len(queue)} songs in the queue.",
                discord.Color.green(),
            )

        try:
            await stream_audio(ctx, client, url)
        except DownloadError:
            await send_error(ctx, "An error occurred while attempting to download audio, check console for details.")
            print(traceback.format_exc())
        except Exception as e:
            await send_error(ctx, f"Error while streaming audio: {str(e)} \n```{traceback.format_exc()}```")


async def setup(bot):
    await bot.add_cog(Play(bot))
    print("Cog loaded: play")
