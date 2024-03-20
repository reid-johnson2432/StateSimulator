"""
Bokeh Plots depicting
entity positions.
"""
import os

import pandas as pd
from bokeh.io import save, output_file
from bokeh.models import ColumnDataSource, HoverTool, SaveTool, BoxZoomTool, Panel, Tabs, ResetTool
from bokeh.palettes import Colorblind8
from bokeh.plotting import figure, column, row


def make_figure(figure_title="", width=750, height=750):
    tools = [HoverTool(tooltips=[('Time', '@time'), ('Value', '@data')]), SaveTool(), BoxZoomTool(), ResetTool()]
    f = figure(title=figure_title, tools=tools, width=width, height=height)
    f.title.text_font_size = '16pt'
    f.title.text_font_style = 'bold'

    f.xaxis.axis_label = 'Time (s)'
    f.xaxis.major_label_text_font_size = '16pt'
    f.xaxis.axis_label_text_font_size = '16pt'
    f.xaxis.axis_label_text_font_style = 'bold'

    if 'Pos' in figure_title or any([keyword in figure_title for keyword in ['Latitude', 'Longitude', 'Altitude']]):
        label = 'Position (m)'
    elif 'Vel' in figure_title:
        label = 'Velocity (m/s)'
    f.yaxis.axis_label = label
    f.yaxis.major_label_text_font_size = '16pt'
    f.yaxis.axis_label_text_font_size = '16pt'
    f.yaxis.axis_label_text_font_style = 'bold'
    return f


def add_kinematics_data(fig, kinematics_data, truth_data, dimension, include_truth=True):
    colors = Colorblind8
    for seed, seed_data in kinematics_data.groupby('Seed'):
        time_data = list(seed_data['Time'].values)
        dimension_data = list(seed_data[dimension].values)
        cds = ColumnDataSource(dict(time=time_data, data=dimension_data))
        fig.line(x='time', y='data', color=colors[int(seed % len(colors))], alpha=0.4,
                 line_width=6, source=cds)

    if include_truth:
        time_data = list(truth_data['Time'].values)
        data = list(truth_data[dimension].values)
        truth_cds = ColumnDataSource(dict(time=time_data, data=data))
        fig.line(x='time', y='data', color='black', line_dash='dashed', line_width=4, source=truth_cds)

    return fig


def add_bias_plot(fig, kinematics_data, truth_data, dimension):
    # --- Bias Plot ---
    analysis_df = kinematics_data.copy(deep=True).reset_index()
    times = list()
    biases = list()
    for time, time_data in analysis_df.groupby('Time'):
        if time == 120:
            continue
        average_estimate = time_data[dimension].mean()
        truth_value = truth_data[truth_data['Time'] == time][dimension].values[0]
        bias = average_estimate - truth_value
        times.append(time)
        biases.append(bias)

    cds = ColumnDataSource(dict(times=times, data=biases))
    fig.line(x='times', y='data', line_width=5, color=Colorblind8[0], source=cds)
    return fig


def make_dashboard(kinematics_report, output_location=None, width=750, height=750):
    project_path = os.path.abspath(__file__).split('metrics')[0]
    truth_kinematics_report_path = os.path.join(project_path, 'external_data', 'terminal_phase.csv')
    truth_data = pd.read_csv(truth_kinematics_report_path)

    position_plots = list()
    position_error_plots = list()
    dimensions = ['Latitude', 'Longitude', 'Altitude']
    for dim in dimensions:
        position_plot = make_figure(f"{dim} vs Time", width=width, height=height)
        position_plot = add_kinematics_data(position_plot, kinematics_report, truth_data, dim)
        position_error_plot = make_figure(f"{dim} Bias vs Time", width=width, height=height)
        position_error_plot = add_bias_plot(position_error_plot, kinematics_report, truth_data, dim)
        position_plots.append(position_plot)
        position_error_plots.append(position_error_plot)

    velocity_plots = list()
    velocity_error_plots = list()
    dimensions = ['VelX', 'VelY', 'VelZ']
    for dim in dimensions:
        velocity_plot = make_figure(f"{dim} vs Time", width=width, height=height)
        velocity_plot = add_kinematics_data(velocity_plot, kinematics_report, truth_data, dim)
        velocity_error_plot = make_figure(f"{dim} Bias vs Time", width=width, height=height)
        velocity_error_plot = add_bias_plot(velocity_error_plot, kinematics_report, truth_data, dim)
        velocity_plots.append(velocity_plot)
        velocity_error_plots.append(velocity_error_plot)

    position_figs = list(zip(*[position_plots, position_error_plots]))
    position_tab = Panel(child=column(*[row(*row_figs) for row_figs in position_figs]), title='Position')
    velocity_figs = list(zip(*[velocity_plots, velocity_error_plots]))
    velocity_tab = Panel(child=column(*[row(*row_figs) for row_figs in velocity_figs]), title='Velocity')
    tabs = [position_tab, velocity_tab]
    if output_location:
        dashboard = Tabs(tabs=tabs)
        output_file(os.path.join(output_location, 'dashboard.html'), mode='inline')
        save(dashboard)
    return tabs
