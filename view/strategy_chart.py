from nicegui import ui


def strategy_chart_view(list_data: list[dict]):
    # 准备数据
    dates = [item["update_time"].strftime("%Y-%m-%d") for item in list_data]

    # 收集所有策略名称（过滤掉"非策略选股"）
    strategy_names = set()
    for item in list_data:
        for strategy in item["data"]:
            if strategy["策略名称"] != "非策略选股":
                strategy_names.add(strategy["策略名称"])

    # 为每个策略构建数据
    series = []
    for name in sorted(strategy_names):
        strategy_data = []
        for item in list_data:
            rate = None
            for strategy in item["data"]:
                if strategy["策略名称"] == name:
                    rate = strategy["当日收益率"]
                    if rate is not None:
                        rate = round(rate * 100, 2)  # 转换为百分比
                    break
            strategy_data.append(rate)

        series.append({
            "name": name,
            "type": "line",
            "data": strategy_data,
        })

    # 计算总收益率（加权平均）
    total_data = []
    for item in list_data:
        total_capital = 0
        weighted_return = 0
        for strategy in item["data"]:
            if strategy["策略名称"] != "非策略选股" and strategy["当日收益率"] is not None:
                capital = strategy["占用资金"]
                total_capital += capital
                weighted_return += capital * strategy["当日收益率"]

        if total_capital > 0:
            total_data.append(round(weighted_return / total_capital * 100, 2))
        else:
            total_data.append(None)

    series.append({
        "name": "总收益率",
        "type": "line",
        "data": total_data,
        "lineStyle": {"width": 3},
        "itemStyle": {"color": "#FF4500"},
    })

    ui.echart(
        {
            "title": {"text": "策略收益率对比"},
            "tooltip": {"trigger": "axis"},
            "legend": {"data": [s["name"] for s in series]},
            "xAxis": {"type": "category", "data": dates},
            "yAxis": {"type": "value", "axisLabel": {":formatter": 'value => value + "%"'}},
            "series": series,
        }
    )


def strategy_allocation_view(list_data: list[dict]):
    # 准备数据
    dates = [item["update_time"].strftime("%Y-%m-%d") for item in list_data]

    # 收集所有策略名称（过滤掉"非策略选股"）
    strategy_names = set()
    for item in list_data:
        for strategy in item["data"]:
            if strategy["策略名称"] != "非策略选股":
                strategy_names.add(strategy["策略名称"])

    # 为每个策略构建实际占比和未使用占比数据
    series = []
    for name in sorted(strategy_names):
        actual_data = []
        unused_data = []
        for item in list_data:
            actual = None
            unused = None
            for strategy in item["data"]:
                if strategy["策略名称"] == name:
                    actual = round(strategy["实际占比"] * 100, 2)
                    unused = round((strategy["理论占比"] - strategy["实际占比"]) * 100, 2)
                    break
            actual_data.append(actual)
            unused_data.append(unused)

        series.append({
            "name": name,
            "type": "bar",
            "stack": name,
            "data": actual_data,
        })
        series.append({
            "name": "未使用",
            "type": "bar",
            "stack": name,
            "data": unused_data,
            "itemStyle": {"color": "#d3d3d3"},
        })

    # 计算总仓位
    total_actual_data = []
    total_unused_data = []
    for item in list_data:
        strategies = [s for s in item["data"] if s["策略名称"] != "非策略选股"]
        total_actual = round(sum(s["实际占比"] for s in strategies) * 100, 2)
        total_theoretical = round(sum(s["理论占比"] for s in strategies) * 100, 2)
        total_actual_data.append(total_actual)
        total_unused_data.append(round(total_theoretical - total_actual, 2))

    series.append({
        "name": "总仓位",
        "type": "bar",
        "stack": "总仓位",
        "data": total_actual_data,
        "itemStyle": {"color": "#FF4500"},
    })
    series.append({
        "name": "未使用",
        "type": "bar",
        "stack": "总仓位",
        "data": total_unused_data,
        "itemStyle": {"color": "#d3d3d3"},
    })

    ui.echart(
        {
            "title": {"text": "策略配置对比"},
            "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
            "legend": {"data": [s["name"] for s in series]},
            "xAxis": {"type": "category", "data": dates},
            "yAxis": {"type": "value", "axisLabel": {":formatter": 'value => value + "%"'}},
            "series": series,
        }
    )
