import os
import sys
import json

from pathlib import Path

from .config_loader import ConfigLoader


class Application:
    """
    应用类，用于管理应用
    """

    def __init__(self):
        self._loaded = False

    def initialize(self, root_path: Path, config_path: Path):
        self._root_path = root_path

        self._raw_config = ConfigLoader(config_path, strict=False).load()
        self._config = self._raw_config[os.getenv("ROCKET_ENV", "development")]

        self._loaded = True

    def _check_loaded(self):
        if not self._loaded:
            raise RuntimeError("应用未初始化")

    @property
    def config(self) -> dict[str, any]:
        self._check_loaded()
        return self._config

    @property
    def root_path(self) -> Path:
        self._check_loaded()
        return self._root_path

    @property
    def qmt_endpoint(self) -> str:
        return self.config["qmt_endpoint"]

    @property
    def qmt_xtdata_endpoint(self) -> str:
        return self.config["qmt_xtdata_endpoint"] or self.qmt_endpoint

    @property
    def python_exe_path(self) -> str:
        return self.config["python_exe_path"] or sys.executable

    @property
    def use_uv(self) -> bool:
        return str(self.config["use_uv"]).lower() == "true"

    def print_config(self):
        print(self.config_json())

    def config_json(self) -> str:
        return json.dumps(
            self.config
            | {
                "run_mode": os.getenv("ROCKET_ENV", "development"),
                "root_path": str(self.root_path),
            },
            indent=4,
            ensure_ascii=False,
        )

    @property
    def should_load_data(self) -> bool:
        return os.getenv("SHOULD_LOAD_DATA", "false").lower() == "true"
