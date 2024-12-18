import os
from pathlib import Path
from typing import Literal, Tuple, Type

from app_paths import AppPaths, get_paths
from pydantic import BaseModel
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)

from .resources.airbyte import AirbyteServer
from .resources.asset_manager import AssetManager
from .resources.mixpeek import MixpeekResource
from .resources.retool import RetoolResources
from .resources.simba import SimbaAPI
from .resources.snowflake import SnowflakeResource
from .resources.temporal import TemporalServer
from .resources.vellum import VellumAPI

app_paths: AppPaths = get_paths("tubescience_cli", "TubeScience")

env_paths: tuple[Path, ...] = ( app_paths.site_config_path / ".env", app_paths.user_config_path / ".env", Path.cwd() / ".env",)
env_path = os.getenv("TS_ENV_FILE", None)
if env_path is not None and Path(env_path).exists():
    env_paths = (Path(env_path),) + env_paths
secrets_paths: tuple[Path, ...] = (Path("/var/run"), Path("/run/secrets"))
settings_paths: tuple[Path, ...] = (
    app_paths.site_config_path / "settings.toml",
    app_paths.user_config_path / "settings.toml",
)


class LoggingSettings(BaseModel):
    log_level: Literal["debug", "info", "warn", "error"] | None = "info"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    log_date_format: str = "%Y-%m-%d %H:%M:%S"


class SiteResources(BaseSettings):

    model_config = SettingsConfigDict(
        env_prefix="TS_",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_file=tuple(str(p) for p in env_paths if p.exists()),
        secrets_dir=tuple(str(p) for p in secrets_paths if p.exists()),
        toml_file=tuple(str(p) for p in settings_paths if p.exists()),
        extra="allow",
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            file_secret_settings,
            TomlConfigSettingsSource(settings_cls),
        )

    debug: bool = False
    testing: bool = False
    logging: LoggingSettings = LoggingSettings()
    snowflake: SnowflakeResource = SnowflakeResource()
    temporal: TemporalServer = TemporalServer()
    retool: RetoolResources = RetoolResources()
    mixpeek: MixpeekResource = MixpeekResource()
    vellum: VellumAPI = VellumAPI()
    simba: SimbaAPI = SimbaAPI()
    asset_manager: AssetManager = AssetManager()
    airbyte: AirbyteServer = AirbyteServer()


site_resources = SiteResources()
