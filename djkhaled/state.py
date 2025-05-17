from dataclasses import dataclass, field
from typing import Optional

import discord


@dataclass
class Track:
    url: str
    requester: discord.User | discord.Member


@dataclass
class GuildState:
    playing: Optional[Track] = None
    client: Optional[discord.VoiceClient] = None
    queue: list[Track] = field(default_factory=list)


state: dict[int, GuildState] = {}
