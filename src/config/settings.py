import os
from pathlib import Path
from typing import Any

from pydantic import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = Path(__file__).resolve().parent.parent.parent


class OLAPResearchSettings(BaseSettings):
    FAKE_DATA_PATH: str = ""
    QUERIES_PATH: str = ""
    BENCH_SIZE: int = 1000000

    class Config:
        env_prefix = 'OLAP_RESEARCH'
        env_file = os.path.join(ROOT_DIR, ".env")
        env_file_encoding = "utf-8"


class CHSettings(BaseSettings):
    CH_CLUSTER_NAME: str
    CH_DB_NAME: str
    CH_REPLICA_DB_NAME: str
    CH_NODE_HOST_NAME: str
    CH_NODE_EXPOSE_PORTS: list[int]
    CH_CONFIG_PATH: str
    CH_LOCAL_MODE: bool = False
    ENVIRONMENT: str = ""

    class Config:
        env_file = os.path.join(ROOT_DIR, ".env")
        env_file_encoding = "utf-8"

        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str) -> Any:
            if field_name.upper() == "CH_NODE_EXPOSE_PORTS":
                return [int(x) for x in raw_val.split(",")]
            return cls.json_loads(raw_val)  # type: ignore  # noqa


ch_settings = CHSettings()
olap_research_settings = OLAPResearchSettings()
