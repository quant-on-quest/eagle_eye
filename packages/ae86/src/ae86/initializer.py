"""
初始化器，用于初始化框架
"""

import os
import sentry_sdk

from pathlib import Path
from .project_creater import create_config_file
from .application import Application


class Initializer:
    """
    初始化器
    """

    def __init__(self, root_path: Path, config_path: Path | None = None):
        self.root_path = root_path
        self.config_path = self._get_config_path(config_path)

        self._init_packages()

    def _get_config_path(self, config_path: Path | None = None) -> Path:
        if config_path is None:
            path = self.root_path / "runtime" / "config.yml.j2"
            if path.exists():
                return path
            else:
                create_config_file(path)
                return path
        return config_path

    def _init_packages(self):
        """
        初始化包
        """
        if os.getenv("AE86_ENV", "development") == "development":
            import sys
            from dotenv import load_dotenv
            from IPython import embed

            sys.breakpointhook = embed

            load_dotenv()

        sentry_sdk.init(os.getenv("SENTRY_DSN"))


app = Application()


def initialize(root_path: Path, config_path: Path | None = None) -> Application:
    """
    初始化框架
    """
    initializer = Initializer(root_path, config_path)
    app.initialize(root_path, initializer.config_path)
    return app
