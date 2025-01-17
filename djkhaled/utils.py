import asyncio
import traceback

import discord
import yt_dlp


async def stream_audio(ctx, vc, url: str):
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
            vc.play(source, after=lambda e: asyncio.run(after_song(vc)))
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
