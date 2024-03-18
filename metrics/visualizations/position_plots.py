"""
Bokeh Plots depicting
entity positions.
"""
import os

import pandas as pd
from bokeh.io import save, output_file
from bokeh.models import ColumnDataSource, HoverTool, SaveTool, BoxZoomTool, Panel, Tabs
from bokeh.plotting import figure, column


def one_d_plot(time_data, kinematics_data, truth_data, figure_title="", width=1500, height=500):
    tools = [HoverTool(tooltips=[('Time', '@time'), ('Value', '@data')]), SaveTool(), BoxZoomTool()]

    f = figure(title=figure_title, tools=tools, width=width, height=height)
    cds = ColumnDataSource(dict(time=time_data, data=kinematics_data))
    f.line(x='time', y='data', color='red', line_width=4, source=cds)
    truth_cds = ColumnDataSource(dict(time=time_data, data=truth_data))
    f.line(x='time', y='data', color='black', line_dash='dashed', line_width=4, source=truth_cds)

    f.title.text_font_size = '16pt'
    f.title.text_font_style = 'bold'

    f.xaxis.axis_label = 'Time (s)'
    f.xaxis.major_label_text_font_size = '16pt'
    f.xaxis.axis_label_text_font_size = '16pt'
    f.xaxis.axis_label_text_font_style = 'bold'

    if 'Pos' in figure_title:
        label = 'Position (m)'
    elif 'Vel' in figure_title:
        label = 'Velocity (m/s)'
    f.yaxis.axis_label = label
    f.xaxis.major_label_text_font_size = '16pt'
    f.yaxis.axis_label_text_font_size = '16pt'
    f.yaxis.axis_label_text_font_style = 'bold'
    return f


def make_position_plots(kinematics_report, output_location=None, width=1500, height=750):
    project_path = os.path.abspath(__file__).split('metrics')[0]
    truth_kinematics_report_path = os.path.join(project_path, 'external_data', 'terminal_phase.csv')
    truth_data = pd.read_csv(truth_kinematics_report_path)

    time = list(kinematics_report['Time'].values)

    position_plots = list()
    dimensions = ['PosX', 'PosY', 'PosZ']
    for dim in dimensions:
        f = one_d_plot(time, list(kinematics_report[dim].values), truth_data[dim].values,
                       figure_title=f"{dim} vs Time", width=width, height=height)
        position_plots.append(f)

    velocity_plots = list()
    dimensions = ['VelX', 'VelY', 'VelZ']
    for dim in dimensions:
        f = one_d_plot(time, list(kinematics_report[dim].values), truth_data[dim].values,
                       figure_title=f"{dim} vs Time", width=width, height=height)
        velocity_plots.append(f)

    position_tab = Panel(child=column(*position_plots), title='Position')
    velocity_tab = Panel(child=column(*velocity_plots), title='Velocity')
    dashboard = Tabs(tabs=[position_tab, velocity_tab])
    if output_location:
        output_file(os.path.join(output_location, 'dashboard.html'), mode='inline')
        save(dashboard)
    return dashboard
