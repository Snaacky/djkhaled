# djhkhaled
A music bot for Discord powered by yt-dlp

## Requirements
* Python 3.11 (or greater)
* uv

## Supports
* YouTube
* Soundcloud
* Deezer
* Dailymotion
* Streamable
* Twitch
* Vimeo
* [and most services listed here](https://github.com/ytdl-org/youtube-dl/tree/master/youtube_dl/extractor)


## Installation
1. Create a Discord bot token at https://discord.com/developers
2. `git clone https://github.com/snaacky/djkhaled` to clone this repository locally.
3. `uv venv` to create a virtual environment for the bot.
4. `uv sync` to install the dependencies.
5. `.venv\Scripts\activate` to activate the virtual environment.
6. Rename `config.example.toml` to `config.toml` and enter your bot token into the config.
7. `python -m djhkhaled` to start the bot.