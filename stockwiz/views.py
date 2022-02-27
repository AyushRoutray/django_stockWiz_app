from django.shortcuts import render
import json
import urllib.request
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import HoverTool
from bokeh.models.annotations import Label
# Create your views here.
def home(request):
    if request.method == 'POST':
        ss = request.POST['stocks']
        datem = request.POST['date']
        source = urllib.request.urlopen('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+ss+'&apikey=HMAFUHSNQ3AB6WTD').read()
        data = json.loads(source)
        source_data = {'open':data['Time Series (Daily)'][datem]['1. open'],
                       'close':data['Time Series (Daily)'][datem]['4. close'],
                       'high':data['Time Series (Daily)'][datem]['2. high'],
                       'low':data['Time Series (Daily)'][datem]['3. low']}
        values = source_data.values()
        values_list = list(values)
        plot = figure(x_axis_label=datem, y_axis_label="Price", title=ss)
        plot.line([-1, 0, 1, 2], [values_list[3], values_list[0], values_list[1], values_list[2]], color="purple")
        plot.circle([0], [values_list[0]], size=10, color= "blue", legend_label="Open: $"+values_list[0])
        plot.circle([1],[values_list[1]], size=10, color= "red", legend_label="Close: $"+values_list[1])
        plot.circle([2],[values_list[2]], size=10, color= "green", legend_label="High: $"+values_list[2])
        plot.circle([-1],[values_list[3]], size=10, color= "yellow", legend_label="Low: $"+values_list[3])
        plot.legend.background_fill_alpha = 0.0
        plot.legend.location = "top_left"
        label1 = Label(x=0, y=float(values_list[0]), x_offset=10, y_offset=-30, text=values_list[0])
        label2 = Label(x=1, y=float(values_list[1]), x_offset=10, y_offset=-30, text=values_list[1])
        label3 = Label(x=2, y=float(values_list[2]), x_offset=10, y_offset=-30, text=values_list[2])
        label4 = Label(x=-1, y=float(values_list[3]), x_offset=10, y_offset=-30, text=values_list[3])
        plot.add_layout(label1)
        plot.add_layout(label2)
        plot.add_layout(label3)
        plot.add_layout(label4)
        script, div = components(plot)
        return render(request, 'stockwiz/dashboard.html' , {'script': script, 'div':div, 'source_data':source_data})
    else:
        source_data = {}
    return render(request, 'stockwiz/dashboard.html', source_data)