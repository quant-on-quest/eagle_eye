import os


def get(
    name: str, raise_error: bool = True, raise_message: str | None = None, default: str = ""
) -> str:
    value = os.getenv(name)
    if not value and raise_error:
        print(raise_message or f"环境变量 {name} 未设置")
        exit(1)
    return value or default
