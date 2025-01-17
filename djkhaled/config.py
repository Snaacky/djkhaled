import tomllib
from pathlib import Path

from pydantic import BaseModel, ConfigDict


class ParentModel(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")


class Discord(ParentModel):
    token: str


class DJKhaledConfig(ParentModel):
    discord: Discord


workspace = Path(__file__).parent.parent
config_file = workspace / "config.toml"

if not config_file.is_file():
    raise FileNotFoundError(f"Cannot load config from {config_file} because it doesn't exist!")

config = DJKhaledConfig.model_validate(tomllib.load(config_file.open("rb")))
