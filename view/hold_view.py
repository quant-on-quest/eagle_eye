import pandas as pd
from nicegui import ui

def hold_view(data: pd.DataFrame):
    table = ui.table.from_pandas(data)

    # 隐藏标签颜色列
    for col in table.columns:
        if col['name'] == '标签颜色':
            col['classes'] = 'hidden'
            col['headerClasses'] = 'hidden'

    # 为"几天后卖出"列添加颜色标签
    table.add_slot('body-cell-几天后卖出', '''
        <q-td :props="props">
            <q-badge
                :style="'background-color: ' + props.row.标签颜色"
                text-color="white"
            >
                {{ props.value }}
            </q-badge>
        </q-td>
    ''')

    table.add_slot('body-cell-证券代码', '''
        <q-td :props="props">
            <a :href="`https://xueqiu.com/S/${props.value.split('.')[1].toUpperCase()}${props.value.split('.')[0]}`"
                target="_blank"
                style="color: #1976d2; text-decoration: underline;">
                {{ props.value }}
            </a>
        </q-td>
    ''')

    return table