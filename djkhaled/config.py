import tomllib
from pathlib import Path

from pydantic import BaseModel, ConfigDict, FilePath


class ParentModel(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")


class Discord(ParentModel):
    token: str
    prefix: str


class YouTube(ParentModel):
    cookies: FilePath = None


class DJKhaledConfig(ParentModel):
    discord: Discord
    youtube: YouTube


workspace = Path(__file__).parent.parent
config_file = workspace / "config.toml"

if not config_file.is_file():
    raise FileNotFoundError(f"Cannot load config from {config_file} because it doesn't exist!")

config = DJKhaledConfig.model_validate(tomllib.load(config_file.open("rb")))
