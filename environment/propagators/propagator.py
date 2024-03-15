"""
Propagators are used to
manage entity locations.
"""

import numpy as np
from pymap3d.ecef import ecef2geodetic


class Propagator:
    def __init__(self, entity, **kwargs):
        """
        Abstract class to manage entity kinematics.
        :param entity: Platform in simulation.
        """
        self.entity = entity
        self.position = kwargs.get('position', np.array([np.nan, np.nan, np.nan]))  # ECEF position
        self.velocity = kwargs.get('velocity', np.array([np.nan, np.nan, np.nan]))  # ECEF velocity

        self.trajectory_data = None

    def set_position(self, position: np.array):
        self.position = position

    def set_velocity(self, velocity: np.array):
        self.velocity = velocity

    def get_position(self):
        return self.position

    def get_velocity(self):
        return self.velocity

    def get_geo_position(self):
        return ecef2geodetic(*self.position)

    def update_position(self, current_time: float, timestep: float):
        raise NotImplementedError
