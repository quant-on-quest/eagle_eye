import boot

from nicegui import ui, html
from pathlib import Path

from model.strategy import get_strategy_performance_history_data
from view.strategy_chart import strategy_chart_view, strategy_allocation_view

def root():
    rocket_pro_path = Path(boot.app.config["rocket_pro_path"]) / "data" / "策略表现_历史.json"
    data = get_strategy_performance_history_data(rocket_pro_path)

    with html.div().classes('flex flex-row w-full'):
        with html.div().classes('basis-1/2 p-1'):
            with ui.card().classes():
                strategy_chart_view(data)
        with html.div().classes('basis-1/2 p-1'):
            with ui.card():
                strategy_allocation_view(data)

ui.run(root, title="策略表现")
