"""
Bokeh Plots depicting
entity positions.
"""
import os

import pandas as pd
from bokeh.io import save, output_file
from bokeh.models import ColumnDataSource, HoverTool, SaveTool, BoxZoomTool, Panel, Tabs
from bokeh.plotting import figure, column
from bokeh.palettes import Colorblind8


def make_figure(figure_title="", width=750, height=750):
    tools = [HoverTool(tooltips=[('Time', '@time'), ('Value', '@data')]), SaveTool(), BoxZoomTool()]
    f = figure(title=figure_title, tools=tools, width=width, height=height)
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


def add_kinematics_data(fig, kinematics_data, truth_data, dimension, include_truth=True):
    colors = Colorblind8
    for seed, seed_data in kinematics_data.groupby('Seed'):
        time_data = list(seed_data['Time'].values)
        dimension_data = list(seed_data[dimension].values)
        cds = ColumnDataSource(dict(time=time_data, data=dimension_data))
        fig.line(x='time', y='data', color=colors[int(seed % len(colors))], alpha=0.6,
                 line_width=4, source=cds, legend_label=f'{seed}')

    if include_truth:
        time_data = list(truth_data['Time'].values)
        data = list(truth_data[dimension].values)
        truth_cds = ColumnDataSource(dict(time=time_data, data=data))
        fig.line(x='time', y='data', color='black', line_dash='dashed', line_width=4, source=truth_cds)

    return fig


def make_dashboard(kinematics_report, output_location=None, width=750, height=750):
    project_path = os.path.abspath(__file__).split('metrics')[0]
    truth_kinematics_report_path = os.path.join(project_path, 'external_data', 'terminal_phase.csv')
    truth_data = pd.read_csv(truth_kinematics_report_path)

    position_plots = list()
    dimensions = ['PosX', 'PosY', 'PosZ']
    for dim in dimensions:
        position_plot = make_figure(f"{dim} vs Time", width=width, height=height)
        position_plot = add_kinematics_data(position_plot, kinematics_report, truth_data, dim)
        position_plots.append(position_plot)

    velocity_plots = list()
    dimensions = ['VelX', 'VelY', 'VelZ']
    for dim in dimensions:
        velocity_plot = make_figure(f"{dim} vs Time", width=width, height=height)
        velocity_plot = add_kinematics_data(velocity_plot, kinematics_report, truth_data, dim)
        velocity_plots.append(velocity_plot)

    position_tab = Panel(child=column(*position_plots), title='Position')
    velocity_tab = Panel(child=column(*velocity_plots), title='Velocity')
    tabs = [position_tab, velocity_tab]
    if output_location:
        dashboard = Tabs(tabs=tabs)
        output_file(os.path.join(output_location, 'dashboard.html'), mode='inline')
        save(dashboard)
    return tabs
