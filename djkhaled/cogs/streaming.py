import asyncio
import traceback

import discord
import yt_dlp
from discord.ext import commands
from yt_dlp.utils import DownloadError

from djkhaled.utils import send_embed, send_error


class Streaming(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.current_stream_process = None
        self.song_queue = []
        self.voice_clients = {}

    async def stream_audio_to_discord(self, ctx, vc, url: str):
        """
        Streams audio to Discord using yt-dlp and ffmpeg.
        """
        opts = {"format": "bestaudio/best", "outtmpl": "pipe:1", "quiet": True, "noplaylist": True}
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=False)

            title = info.get("title", "Unknown Title")
            duration = info.get("duration", 0)
            formatted_duration = f"{duration // 60:02}:{duration % 60:02}"

            try:
                source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(info["url"]))
                vc.play(source, after=lambda e: asyncio.run(self.after_song(vc)))
            except Exception as e:
                print(f"Error starting audio stream: {str(e)} \n```{traceback.format_exc()}```")
                return await vc.disconnect()

            embed = discord.Embed(
                title="🎶 Now Playing",
                description=f"Added **{title}** ({formatted_duration}) to begin playing.",
                color=discord.Color.green(),
            )
            await ctx.channel.send(embed=embed)

    async def after_song(self, vc):
        """
        Call after a song finishes playing.
        It will play the next song in the queue, if there is one.
        """
        if self.song_queue:
            next_song = self.song_queue.pop(0)
            await self.stream_audio_to_discord(vc.channel, vc, next_song["url"])
        else:
            await vc.disconnect()

    @commands.command(name="play")
    async def play(self, ctx, url: str):
        """
        Command to play a URL in a voice channel.
        """
        if not ctx.author.voice:
            return await send_error(ctx, "You need to join a voice channel first.")

        channel = ctx.author.voice.channel

        if ctx.guild.id not in self.voice_clients:
            permissions = channel.permissions_for(ctx.guild.me)
            if not permissions.view_channel:
                return await send_error(ctx, "I do not have permission to view that voice channel.")
            if not permissions.connect:
                return await send_error(ctx, "I do not have permission to connect to that voice channel.")
            if not permissions.speak:
                return await send_error(ctx, "I do not have permission to speak in that voice channel.")
            client = await channel.connect()
            self.voice_clients[ctx.guild.id] = client

        if ctx.guild.id in self.voice_clients and client.is_playing():
            self.song_queue.append({"url": url, "requester": ctx.author})
            return await send_embed(
                ctx,
                "✅ Added to Queue",
                f"Added to the queue. There are {len(self.song_queue)} songs in the queue.",
                discord.Color.green(),
            )

        try:
            await self.stream_audio_to_discord(ctx, client, url)
        except DownloadError:
            await send_error(ctx, "An error occurred while attempting to download audio, check console for details.")
            print(traceback.format_exc())
        except Exception as e:
            await send_error(ctx, f"Error while streaming audio: {str(e)} \n```{traceback.format_exc()}```")

    @commands.command(name="skip")
    async def skip(self, ctx):
        """
        Skip the current playing audio without disconnecting from the voice channel.
        """
        if not ctx.voice_client or not ctx.voice_client.is_playing():
            return await send_error(ctx, "No audio is currently playing.")

        ctx.voice_client.stop()
        await send_embed(ctx, "⏭️ Skipped", "Skipped the current track.", discord.Color.green())

    @commands.command(name="seek")
    async def seek(self, ctx, time: int):
        """
        Seek to a specific time in the current audio.
        """
        if not self.current_stream_process:
            return await send_error(ctx, "No audio is currently playing.")

        self.current_stream_process.kill()
        self.current_stream_process = None

        await self.stream_audio_to_discord(ctx.voice_client, ctx.message.content.split(" ")[1], time)
        await send_embed(
            ctx,
            "✅ Seeked",
            f"Jumped to {time} seconds in the audio.",
            discord.Color.green(),
        )

    @commands.command(name="stop")
    async def stop(self, ctx):
        """
        Stop the currently playing audio and disconnect.
        """
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await send_embed(
                ctx,
                "✅ Stopped",
                "Disconnected from the voice channel.",
                discord.Color.green(),
            )
        else:
            await send_embed(
                ctx,
                "❌ Error",
                "I am not connected to a voice channel.",
                discord.Color.red(),
            )

    @commands.command(name="queue")
    async def queue(self, ctx):
        """
        Command to show the current song queue.
        """
        if not ctx.voice_client or not ctx.voice_client.is_playing():
            return await send_error(ctx, "No audio is currently playing.")

        queue_embed = discord.Embed(
            title="🎶 Current Song Queue",
            description="Here are the songs in the queue:",
            color=discord.Color.blue(),
        )

        if self.song_queue:
            current_song = self.song_queue[0]
            queue_embed.add_field(
                name="Now Playing",
                value=f"**{current_song['url']}** (Requested by: {current_song['requester'].name})",
                inline=False,
            )

        for index, song in enumerate(self.song_queue[1:], start=2):
            song_info = f"**{index}.** {song['url']} (Requested by: {song['requester'].name})"
            queue_embed.add_field(name=f"Song {index}", value=song_info, inline=False)

        await ctx.send(embed=queue_embed)

    @commands.command(name="remove")
    async def queue_remove(self, ctx, index: int):
        """
        Remove a song from the queue by its ID/index.
        """
        if index < 1 or index > len(self.song_queue):
            return await send_error(ctx, "Invalid song index. Please provide a valid index from the queue.")

        removed_song = self.song_queue.pop(index - 1)
        await send_embed(
            ctx,
            "✅ Removed from Queue",
            f"Removed **{removed_song['url']}** from the queue.",
            discord.Color.green(),
        )


async def setup(bot):
    await bot.add_cog(Streaming(bot))
    print("Cog loaded: streaming")
