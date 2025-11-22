import pandas as pd
from pathlib import Path
from datetime import datetime
import random
import json
import re

def get_current_hold_data(path: Path, performance_path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, encoding="gbk")

    # 将计划卖出日期转换为 datetime 类型
    df['计划卖出日期'] = pd.to_datetime(df['计划卖出日期'])

    # 计算距离卖出日期还有几天
    today = pd.Timestamp(datetime.now().date())
    days_until_sell = (df['计划卖出日期'] - today).dt.days

    # 在计划卖出日期列后面插入几天后卖出列
    sell_date_index = df.columns.get_loc('计划卖出日期')
    df.insert(sell_date_index + 1, '几天后卖出', days_until_sell) # type: ignore

    # 解析"其他"列，提取offset信息
    def parse_other_field(other: str) -> str:
        """从'其他'列解析offset，如：股票名称=中京电子+择时信号=1+offset=W_1+滑点=8.82"""
        if pd.isna(other):
            return ''
        match = re.search(r'offset=([^+]+)', str(other))
        return match.group(1) if match else ''

    df['offset'] = df['其他'].apply(parse_other_field)

    # 读取个股表现历史数据
    if performance_path.exists():
        with open(performance_path, 'r', encoding='utf-8') as f:
            performance_data = json.load(f)
        
        sorted_performance_data = sorted(performance_data, key=lambda x: x['update_time'])
        latest_performance = sorted_performance_data[-1] if sorted_performance_data else {}

        latest_performance_data = latest_performance.get('data', [])

        # 创建匹配字典：(策略名称, 证券代码, offset) -> 累计收益率
        performance_map = {}
        for item in latest_performance_data:
            # 只处理有offset字段的新框架数据
            if 'offset' in item and item.get('offset'):
                key = (item['策略名称'], item['证券代码'], item['offset'])
                performance_map[key] = {
                    '累计收益率': item.get('累计收益率', 0),
                    '累计盈亏': item.get('累计盈亏', 0),
                    '当日盈亏': item.get('当日盈亏', 0),
                    '当日收益率': item.get('当日收益率', 0),
                }

        # 匹配并添加累计收益率和累计盈亏
        def get_performance(row):
            if not row['offset']:  # 只处理新框架数据
                return None
            key = (row['策略名称'], row['证券代码'], row['offset'])
            return performance_map.get(key)

        df['表现数据'] = df.apply(get_performance, axis=1)
        df['累计收益率'] = df['表现数据'].apply(lambda x: x['累计收益率'] if x else None)
        df['累计盈亏'] = df['表现数据'].apply(lambda x: x['累计盈亏'] if x else None)

        df['当日盈亏'] = df['表现数据'].apply(lambda x: x['当日盈亏'] if x else None)
        df['当日收益率'] = df['表现数据'].apply(lambda x: x['当日收益率'] if x else None)
        df.drop('表现数据', axis=1, inplace=True)

        # 在证券代码后面插入累计收益率和累计盈亏列
        code_index = df.columns.get_loc('证券代码')
        if '累计收益率' in df.columns:
            cumulative_return = df.pop('累计收益率')
            df.insert(code_index + 1, '累计收益率', cumulative_return) # type: ignore
        if '累计盈亏' in df.columns:
            cumulative_profit = df.pop('累计盈亏')
            df.insert(code_index + 2, '累计盈亏', cumulative_profit) # type: ignore
        if '当日盈亏' in df.columns:
            daily_profit = df.pop('当日盈亏')
            df.insert(code_index + 3, '当日盈亏', daily_profit) # type: ignore
        if '当日收益率' in df.columns:
            daily_return = df.pop('当日收益率')
            df.insert(code_index + 4, '当日收益率', daily_return) # type: ignore    

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

