import asyncio
import traceback

import discord
import yt_dlp
from discord.ext import commands

from djkhaled.config import config
from djkhaled.state import song_queue, voice_clients


async def stream_audio(ctx: commands.Context, client: discord.VoiceClient, url: str):
    """
    Streams audio to Discord using yt-dlp and ffmpeg.
    """
    ytdlp_opts = {
        "format": "bestaudio/best",
        "logtostderr": False,
        "ignoreerrors": True,
        "no_warnings": True,
        "noplaylist": True,
        "outtmpl": "pipe:1",
        "quiet": True,
    }

    if config.youtube.cookies:
        ytdlp_opts["cookiefile"] = config.youtube.cookies

    ffmpeg_opts = {
        "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
        "options": "-vn",
    }

    with yt_dlp.YoutubeDL(ytdlp_opts) as ydl:
        info = ydl.extract_info(url, download=False)

        title = info.get("title", "Unknown Title")
        duration = info.get("duration", 0)
        formatted_duration = f"{duration // 60:02}:{duration % 60:02}"

        try:
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(info["url"], **ffmpeg_opts))
            client.play(source, after=lambda _: after_song(ctx))
        except Exception as e:
            print(f"Error starting audio stream: {str(e)} \n```{traceback.format_exc()}```")

        embed = discord.Embed(
            title="🎶 Now Playing",
            description=f"Added **{title}** ({formatted_duration}) to begin playing.",
            color=discord.Color.green(),
        )
        await ctx.channel.send(embed=embed)


def after_song(ctx: commands.Context):
    """
    Call after a song finishes playing.
    It will play the next song in the queue, if there is one.
    """
    client = voice_clients[ctx.guild.id]
    queue = song_queue[ctx.guild.id]

    if not queue:
        return

    song = queue.pop(0)
    coro = stream_audio(ctx=ctx, client=client, url=song.get("url"))
    fut = asyncio.run_coroutine_threadsafe(coro, client.loop)

    try:
        fut.result()
    except Exception as e:
        print(f"Error starting next song: {str(e)} \n```{traceback.format_exc()}```")
