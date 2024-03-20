"""
Create metrics from reports.
"""

import os

import pandas as pd
from bokeh.io import save, output_file
from bokeh.models import Tabs

from metrics.visualizations.endgame_plots import make_endgame_plot
from metrics.visualizations.multi_run_plots import make_dashboard
from metrics.visualizations.position_plots import make_position_plots
from metrics.visualizations.three_d_position_plot import make_3d_plot
from metrics.visualizations.trajectory_to_kml import create_trajectory_kml
from reports.kinematics_report import KinematicsReport


def post_sim_script(reports: dict, output_location):
    print('Starting PostSim script')
    kinematics_report = reports['KinematicsReport']

    # --- create KML ---
    for entity, entity_data in kinematics_report.groupby('EntityName'):
        trajectory = list()
        for idx, row in entity_data.iterrows():
            lat, lon, alt = row.Latitude, row.Longitude, row.Altitude
            trajectory.append([lat, lon, alt])
        filename = f'{entity}_trajectory'
        create_trajectory_kml(trajectory, os.path.join(output_location, filename + '.kml'))
        make_3d_plot(trajectory, os.path.join(output_location, filename + '.png'))
        make_position_plots(kinematics_report, output_location=output_location)


def post_set_script(set_location):
    from pymap3d.vincenty import vdist
    print('Starting Post Set Script')
    set_data = KinematicsReport().data
    for seed in os.listdir(set_location):
        if seed in ['.DS_Store', 'dashboard.html', 'endgame_statistics.csv', 'endgame_data.csv',
                    'dashboardUpdated.html']:
            continue
        filepath = os.path.join(set_location, seed, f'KinematicsReport_{seed}.csv')
        seed_data = pd.read_csv(filepath)
        seed_data['Seed'] = int(seed)
        set_data = pd.concat([set_data, seed_data])

    endgame_time = 120
    aim_point = (33.23849999999999, -106.3463999999999)

    endgame_data = set_data[set_data['Time'] == endgame_time]

    kinematics_tabs = make_dashboard(set_data)
    endgame_tabs = make_endgame_plot(endgame_data)
    dashboard = Tabs(tabs=[*kinematics_tabs, *endgame_tabs])
    output_file(os.path.join(set_location, 'dashboardUpdated.html'), mode='inline')
    save(dashboard)
    endgame_data['dist'] = endgame_data.apply(lambda row: vdist(*aim_point, row['Latitude'], row['Longitude'])[0], axis=1)
    endgame_statistics = endgame_data.describe()
    endgame_data.to_csv(os.path.join(set_location, 'endgame_data.csv'))
    endgame_statistics.to_csv(os.path.join(set_location, 'endgame_statistics.csv'))


if __name__ == '__main__':
    output_folder = '/Users/reidjohnson/Desktop/SimOutput/FinalRuns2'
    post_set_script(output_folder)
