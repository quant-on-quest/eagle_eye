import warnings

from pathlib import Path


def create_config_file(path: Path):
    """
    创建配置文件
    """
    warnings.warn("还没有实现创建配置文件的功能")
    with open(path, "w") as f:
        f.write("[production]\n[development]\n[test]")
