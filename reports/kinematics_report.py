"""
Report Kinematics data for entities.
"""

import pandas as pd


class KinematicsReport:
    def __init__(self):
        self.data = pd.DataFrame(columns=['Time', 'EntityName', 'Latitude', 'Longitude', 'Altitude',
                                          'PosX', 'PosY', 'PosZ', 'VelX', 'VelY', 'VelZ'])

    def update_report(self, time, entity):
        self._extract_kinematics_data(time, entity)

    def _extract_kinematics_data(self, time, entity):
        entity_name = entity.name
        lat, lon, alt = entity.propagator.get_geo_position()
        pos_x, pos_y, pos_z = entity.propagator.get_position()
        vel_x, vel_y, vel_z = entity.propagator.get_velocity()
        kinematics_data = [time, entity_name, lat, lon, alt, pos_x, pos_y, pos_z, vel_x, vel_y, vel_z]
        index = len(self.data)
        self.data.loc[index] = kinematics_data
