import asyncio
import logging
import traceback
from typing import Optional

import discord
import yt_dlp
from discord.ext import commands

from djkhaled.consts import ffmpeg_opts, ytdlp_opts
from djkhaled.state import Track, state


async def stream_audio(ctx: commands.Context, track: Track, skip_to: Optional[int] = None) -> None:
    """
    Streams audio to Discord using yt-dlp and ffmpeg.
    """
    gstate = state[ctx.guild.id]

    # https://stackoverflow.com/a/73132956/2274960
    with yt_dlp.YoutubeDL(ytdlp_opts) as ydl:
        info = ydl.extract_info(track.url, download=False)

        title = info.get("title", "Unknown Title")
        duration = info.get("duration", 0)
        # TODO: formatted_duration needs to be fixed for Soundcloud
        formatted_duration = f"{duration // 60:02}:{duration % 60:02}"

        if skip_to:
            ffmpeg_opts["before_options"] = ffmpeg_opts["before_options"] + f" -ss {skip_to}"

        try:
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(info["url"], **ffmpeg_opts))
            gstate.client.play(source, after=lambda _: after_song(ctx))
        except Exception as e:
            logging.error(f"Error starting audio stream: {str(e)} \n```{traceback.format_exc()}```")

        embed = discord.Embed(
            title="🎶 Now Playing",
            description=f"Added **{title}** ({formatted_duration}) to begin playing.",
            color=discord.Color.green(),
        )
        await ctx.channel.send(embed=embed)
        gstate.playing = track


def after_song(ctx: commands.Context) -> None:
    """
    Call after a song finishes playing.
    It will play the next song in the queue, if there is one.
    """
    gstate = state[ctx.guild.id]

    if not gstate.queue:
        gstate.playing = None
        return

    track = gstate.queue.pop(0)
    coro = stream_audio(ctx=ctx, track=track)
    fut = asyncio.run_coroutine_threadsafe(coro, gstate.client.loop)

    try:
        fut.result()
    except Exception as e:
        logging.error(f"Error starting next song: {str(e)} \n```{traceback.format_exc()}```")
