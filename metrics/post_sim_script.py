"""
Create metrics from reports.
"""

import os
from metrics.visualizations.trajectory_to_kml import create_trajectory_kml


def post_sim_script(reports: dict, output_location):
    print('Starting PostSim script')
    kinematics_report = reports['KinematicsReport']

    # --- create KML ---
    for entity, entity_data in kinematics_report.groupby('EntityName'):
        trajectory = list()
        for idx, row in entity_data.iterrows():
            lat, lon, alt = row.Latitude, row.Longitude, row.Altitude
            trajectory.append([lat, lon, alt])
        filename = f'{entity}_trajectory.kml'
        create_trajectory_kml(trajectory, os.path.join(output_location, filename))
