"""
Visualize endgame statistics.
"""

import os

import pandas as pd
from bokeh.io import save, output_file
from bokeh.models import ColumnDataSource, HoverTool, SaveTool, BoxZoomTool, Panel, Tabs, WheelZoomTool, ResetTool, PanTool
from bokeh.plotting import figure, column
from bokeh.palettes import Colorblind8


def make_figure(figure_title="", width=750, height=750):
    tools = [HoverTool(tooltips=[('Latitude', '@lat'), ('Longitude', '@lon')]),
             SaveTool(), BoxZoomTool(), WheelZoomTool(), ResetTool(), PanTool()]
    f = figure(title=figure_title, tools=tools, width=width, height=height)
    f.title.text_font_size = '16pt'
    f.title.text_font_style = 'bold'

    f.xaxis.axis_label = 'Longitude'
    f.xaxis.major_label_text_font_size = '16pt'
    f.xaxis.axis_label_text_font_size = '16pt'
    f.xaxis.axis_label_text_font_style = 'bold'

    f.yaxis.axis_label = 'Latitude'
    f.yaxis.major_label_text_font_size = '16pt'
    f.yaxis.axis_label_text_font_size = '16pt'
    f.yaxis.axis_label_text_font_style = 'bold'
    return f


def add_impact_points(fig, endgame_data, truth_data, include_truth=True):
    colors = Colorblind8
    for seed, seed_data in endgame_data.groupby('Seed'):
        latitude = list(seed_data['Latitude'].values)
        longitude = list(seed_data['Longitude'].values)
        cds = ColumnDataSource(dict(lat=latitude, lon=longitude))
        fig.scatter(x='lon', y='lat', color=colors[int(seed % len(colors))], size=20,
                    alpha=0.4, source=cds)

    if include_truth:
        latitude = list(truth_data['Latitude'].values)
        longitude = list(truth_data['Longitude'].values)
        truth_cds = ColumnDataSource(dict(lat=latitude, lon=longitude))
        fig.scatter(x='lon', y='lat', color='red', marker='triangle', size=20, source=truth_cds)

    return fig


def make_endgame_plot(endgame_data,  output_location=None, width=750, height=750):
    project_path = os.path.abspath(__file__).split('metrics')[0]
    truth_kinematics_report_path = os.path.join(project_path, 'external_data', 'terminal_phase.csv')
    truth_data = pd.read_csv(truth_kinematics_report_path)
    truth_data = truth_data[truth_data['Time'] == 120]

    impact_figure = make_figure(figure_title='Impact Locations')
    impact_figure = add_impact_points(impact_figure, endgame_data, truth_data)

    endgame_tab = Panel(child=column(impact_figure), title='Impact Locations')
    if output_location:
        dashboard = Tabs(tabs=[endgame_tab])
        output_file(os.path.join(output_location, 'impact_locations.html'), mode='inline')
        save(dashboard)
    return [endgame_tab]

