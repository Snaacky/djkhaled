import tomllib
from pathlib import Path

from pydantic import BaseModel, ConfigDict, FilePath


class ParentModel(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")


class Discord(ParentModel):
    token: str
    prefix: str


class DJKhaled(ParentModel):
    admins: list[int]


class YouTube(ParentModel):
    cookies: FilePath = None


class DJKhaledConfig(ParentModel):
    discord: Discord
    djkhaled: DJKhaled
    youtube: YouTube


path = Path(__file__).parent.parent / "config.toml"
if not path.is_file():
    raise FileNotFoundError(f"Cannot load {path}!")

config = DJKhaledConfig.model_validate(tomllib.load(path.open("rb")))
