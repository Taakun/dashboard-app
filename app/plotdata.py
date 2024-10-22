import plotly.graph_objects as go
from monthdelta import monthmod
from dateutil.relativedelta import relativedelta


class PlotData():
    def __init__(self, dataset):
        self.dataset = dataset
        self.state_dict = {'infect': '感染者数', 'severe': '重症者数', 'death': '死亡者'}
    
    def plot_pie(self, fig, company_name_1, month):
        labels = list(self.state_dict.keys())
        values = [self.dataset[status][company_name_1].values[month] for status in list(self.state_dict.keys())]
        fig.add_trace(go.Pie(labels=labels, values=values))
        fig.update_traces(marker=dict(colors=['gold', 'mediumturquoise', 'darkorange', 'lightgreen']))
        
    def plot_bar(self, fig, month_list, state1, state2):
        if state2=='visitor':
            y_bar='Visitor_Arrivals'
            name_bar="訪日外客数"
        else:
            y_bar='PCR_inspectors'
            name_bar="PCR検査数"
        fig.add_trace(
            go.Bar(
                x=month_list,
                y=self.dataset[state2][y_bar],
                name=name_bar,
                marker=dict(color="paleturquoise"),
            )
        )
        fig.add_trace(
            go.Scatter(
                x=month_list,
                y=self.dataset[state1]['ALL'],
                yaxis="y2",
                name=self.state_dict[state1],
                marker=dict(color="crimson"),
            )
        )
    
    def month_diff(self, start, end):
        month_num = monthmod(start, end)[0].months+1
        month_list = []
        for i in range(month_num):
            month = start + relativedelta(months=i)
            month_list.append(month.strftime("%Y-%m"))
            
        return month_num, month_list
    