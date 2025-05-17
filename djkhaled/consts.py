from djkhaled.config import config

ffmpeg_opts = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn",
}

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
