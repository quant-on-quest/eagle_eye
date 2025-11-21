import yaml
from jinja2 import Template
from pathlib import Path
from .env import get as get_env


class ConfigLoader:
    """
    配置加载器，支持环境变量替换
    """

    def __init__(self, config_path: str, strict: bool = True):
        """
        :param config_path: 配置文件路径
        :param strict: 是否严格模式（环境变量不存在时抛出异常）
        """
        self.config_path = config_path
        self.strict = strict

        path = Path(config_path)

        if path.exists():
            self.config_text = path.read_text(encoding="utf-8")
        else:
            raise FileNotFoundError(f"配置文件不存在: {config_path}")

    def load(self) -> dict[str, any]:
        template = Template(self.config_text)
        yaml_text = template.render(env=get_env)
        return yaml.safe_load(yaml_text)
