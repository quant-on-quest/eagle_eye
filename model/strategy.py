import json
from datetime import datetime
from pathlib import Path


def get_strategy_performance_history(rocket_pro_path: Path) -> list[dict]:
    with open(rocket_pro_path, "r") as f:
        return json.load(f)

def convert_strategy_performance_history(strategy_performance_history: list[dict]) -> list[dict]:
    "根据update_time排序并转换为datetime对象, 同时保留一天中的最后一条数据"
    last_day_data = {}
    for item in sorted(strategy_performance_history, key=lambda x: x["update_time"]):
        dt = datetime.fromtimestamp(item["update_time"])
        item["update_time"] = dt
        last_day_data[dt.date()] = item
    return list(last_day_data.values())

def get_strategy_performance_history_data(rocket_pro_path: Path) -> list[dict]:
    strategy_performance_history = get_strategy_performance_history(rocket_pro_path)
    return convert_strategy_performance_history(strategy_performance_history)