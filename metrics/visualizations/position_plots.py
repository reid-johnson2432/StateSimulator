"""
Bokeh Plots depicting
entity positions.
"""
from bokeh.models import ColumnDataSource, HoverTool, SaveTool, BoxZoomTool
from bokeh.models import Panel
from bokeh.plotting import figure, column


def one_d_plot(time_data, position_data, figure_title="", tools=None, width=1500, height=500):
    if tools is None:
        tools = list()
    f = figure(title=figure_title, tools=tools, width=width, height=height)
    cds = ColumnDataSource(dict(time=time_data, position=position_data))
    f.line(x='time', y='position', color='red', line_width=8, source=cds)

    f.title.text_font_size = '16pt'
    f.title.text_font_style = 'bold'

    f.xaxis.axis_label = 'Time (s)'
    f.xaxis.major_label_text_font_size = '16pt'
    f.xaxis.axis_label_text_font_size = '16pt'
    f.xaxis.axis_label_text_font_style = 'bold'

    f.yaxis.axis_label = 'Position (m)'
    f.xaxis.major_label_text_font_size = '16pt'
    f.yaxis.axis_label_text_font_size = '16pt'
    f.yaxis.axis_label_text_font_style = 'bold'
    return f


def make_position_plots(kinematics_report, width=1500, height=750):
    tools = [HoverTool(tooltips=[('Time', '@time'), ('Position', '@position')]), SaveTool(), BoxZoomTool()]
    time = list(kinematics_report['Time'].values)

    position_plots = list()
    dimensions = ['PosX', 'PosY', 'PosZ']
    for dim in dimensions:
        f = one_d_plot(time, list(kinematics_report[dim].values), figure_title=f"{dim} vs Time", tools=tools)
        position_plots.append(f)

    tab = Panel(child=column(*position_plots), title='Positions')
    return tab


if __name__ == '__main__':
    import os
    import pandas as pd
    from bokeh.io import save, output_file
    from bokeh.models import Tabs

    output_folder = '/Users/reidjohnson/Desktop/StateSimulator/output'
    kinematics_report_path = os.path.join(output_folder, 'KinematicsReport-2024-03-13 21:40:45.735176.csv')
    df = pd.read_csv(kinematics_report_path)
    pos_tab = make_position_plots(df)

    dashboard = Tabs(tabs=[pos_tab])
    output_location = "PositionPlots.html"
    output_file(output_location, mode='inline')
    save(dashboard)
