from datetime import datetime as dt

import plotly.graph_objects as go
from dash import Dash, Input, Output, callback, dcc, html

from dataloader import DataLoader
from plotdata import PlotData

# Dashアプリを作成
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css'] # cssの設定
app = Dash(__name__, external_stylesheets=external_stylesheets)

# データの読み込み
data_loader = DataLoader('app/dataset.json')
dataset, dataset_dict = data_loader.load_data()

plotdata = PlotData(dataset_dict)
month_num, month_list = plotdata.month_diff(dt(2020,5,1), dt(2021,12,31))

# レイアウトを定義
app.layout = html.Div([html.H1('Python Dash 総集編'),
                       html.H2('都道府県別の感染状況を円グラフで比較(月別)'),
                       html.Div([
                            html.Div(dcc.Dropdown(
                               id='stock_chart_dropdown_1',
                               options=dataset['prefecture'],
                               multi=False,
                               placeholder='都道府県'
                           ),
                               style={'width': '15%', 'display': 'inline-block', 'margin-right': 10})
                       ]),
                       html.Div(dcc.Slider(
                           id='stock_chart_slider',
                           min=1,
                           max=19,
                           value=1,
                           step=1,
                           marks={i+1: {'label': month_list[i]} for i in range(month_num)}
                       ),
                           ),
                       html.Div(id='stock_chart', style={'width': '100%'}),
                       html.H2('感染状況とその他要素を2軸で比較(月別)'),
                       html.Div([
                           html.Div(dcc.Dropdown(
                               id='stock_chart_dropdown_2',
                               options=dataset['status'],
                               multi=False,
                               placeholder='感染状況'
                               ), style={'width': '15%', 'display': 'inline-block', 'margin-right': 10})
                       ]),

                       dcc.RadioItems(
                           id='radio1',
                           options=dataset['other'],
                            value='visitor',
                            labelStyle={'display':'inline-block'} #Radio Buttonを横並びにする
                        ),

                       html.Div(id='complex_chart', style={'width': '100%'})
                       ], style={'margin': '5%'})

# コールバックの設定
@app.callback(
    Output(component_id='stock_chart', component_property='children'),
    Input(component_id='stock_chart_slider', component_property='value'),
    Input(component_id='stock_chart_dropdown_1', component_property='value')
)
def update_graph(month, company_name_1):
    if (company_name_1 == "" or company_name_1 is None):
        return None
    fig = go.Figure()
    plotdata.plot_pie(fig, company_name_1, month)
    real = month_list[month-1]
    fig.update_layout(title=dict(text=f'<b>{real}の感染状況の割合',
                                 font_color='grey'),
                      showlegend=True,
                      plot_bgcolor='white',
                      width=1000,
                      height=500,
                      )
    return dcc.Graph(figure=fig)

@app.callback(
    Output(component_id='complex_chart', component_property='children'),
    Input(component_id='stock_chart_dropdown_2', component_property='value'),
    Input(component_id='radio1', component_property='value')
)
def update_graph2(state1, state2):
    if (state1 == "" or state1 is None) or (state2 == "" or state2 is None):
        return None
    fig2 = go.Figure()
    plotdata.plot_bar(fig2, month_list, state1, state2)
    fig2.update_layout(
                      showlegend=True,
                      legend = dict(
                      yanchor="top", y=0.99,
                      xanchor="left", x=0.05,
                      ),
                      plot_bgcolor='white',
                      width=1000,
                      height=500,
                      yaxis=dict(
                          title=dict(text=f"Total number of {state2} people"),
                          side="left",
    ),
        yaxis2=dict(
                        title=dict(text=f"Total number of {state1}"),
                        side="right",
                        overlaying="y",
                        tickmode="sync",
    ),
    )
    return dcc.Graph(figure=fig2)

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
    