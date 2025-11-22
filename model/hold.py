import pandas as pd
from pathlib import Path
from datetime import datetime
import random

def get_current_hold_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, encoding="gbk")

    # 将计划卖出日期转换为 datetime 类型
    df['计划卖出日期'] = pd.to_datetime(df['计划卖出日期'])

    # 计算距离卖出日期还有几天
    today = pd.Timestamp(datetime.now().date())
    days_until_sell = (df['计划卖出日期'] - today).dt.days

    # 在计划卖出日期列后面插入几天后卖出列
    sell_date_index = df.columns.get_loc('计划卖出日期')
    df.insert(sell_date_index + 1, '几天后卖出', days_until_sell) # type: ignore

    # 为每个不同的日期分配一个随机颜色（保证高对比度）
    unique_dates = df['计划卖出日期'].unique()
    date_color_map = {}

    for date in unique_dates:
        # 随机色相（0-360度，覆盖所有颜色）
        h = random.randint(0, 360)
        # 高饱和度（60-90%），让颜色鲜艳
        s = random.randint(60, 90)
        # 低亮度（35-50%），确保白色文字清晰可见
        lightness = random.randint(35, 50)

        date_color_map[date] = f'hsl({h}, {s}%, {lightness}%)'

    # 添加颜色列
    df.insert(sell_date_index + 2, '标签颜色', df['计划卖出日期'].map(date_color_map)) # type: ignore

    # 按策略名称排序归类
    df = df.sort_values(by='策略名称', ascending=True).reset_index(drop=True)

    return df

