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
        <q-td :props="props" :title="props.col.label">
            <q-badge
                :style="'background-color: ' + props.row.标签颜色"
                text-color="white"
            >
                {{ props.value }}
            </q-badge>
        </q-td>
    ''')

    table.add_slot('body-cell-证券代码', '''
        <q-td :props="props" :title="props.col.label">
            <a :href="`https://xueqiu.com/S/${props.value.split('.')[1].toUpperCase()}${props.value.split('.')[0]}`"
                target="_blank"
                style="color: #1976d2; text-decoration: underline;">
                {{ props.value }}
            </a>
        </q-td>
    ''')

    # 累计收益率 - 显示百分比，正数红色，负数绿色，加粗
    table.add_slot('body-cell-累计收益率', '''
        <q-td :props="props" :title="props.col.label">
            <span :style="{color: props.value > 0 ? 'red' : props.value < 0 ? 'green' : 'black', fontWeight: 'bold'}">
                {{ props.value != null ? (props.value * 100).toFixed(2) + '%' : '-' }}
            </span>
        </q-td>
    ''')

    # 累计盈亏 - 正数红色，负数绿色，加粗
    table.add_slot('body-cell-累计盈亏', '''
        <q-td :props="props" :title="props.col.label">
            <span :style="{color: props.value > 0 ? 'red' : props.value < 0 ? 'green' : 'black', fontWeight: 'bold'}">
                {{ props.value != null ? props.value.toFixed(2) : '-' }}
            </span>
        </q-td>
    ''')

    # 当日盈亏 - 正数红色，负数绿色，加粗
    table.add_slot('body-cell-当日盈亏', '''
        <q-td :props="props" :title="props.col.label">
            <span :style="{color: props.value > 0 ? 'red' : props.value < 0 ? 'green' : 'black', fontWeight: 'bold'}">
                {{ props.value != null ? props.value.toFixed(2) : '-' }}
            </span>
        </q-td>
    ''')

    # 当日收益率 - 显示百分比，正数红色，负数绿色，加粗
    table.add_slot('body-cell-当日收益率', '''
        <q-td :props="props" :title="props.col.label">
            <span :style="{color: props.value > 0 ? 'red' : props.value < 0 ? 'green' : 'black', fontWeight: 'bold'}">
                {{ props.value != null ? (props.value * 100).toFixed(2) + '%' : '-' }}
            </span>
        </q-td>
    ''')

    return table