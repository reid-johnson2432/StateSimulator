"""
Generic Entity.
"""

import numpy as np
import pymap3d
import uuid
# TODO: Use numba for properties ?


class GenericEntity:
    def __init__(self, start_position: tuple, start_kinematics: tuple):
        """
        start_position (3-tuple): (ECEFx, ECEFy, ECEFz) in meters
        aram start_kinematics (3-tuple): (ECEFx_dot, ECEFy_dot, ECEFz_dot) in meters per second
        """
        self.id = uuid.uuid4()
        self.last_position = None
        self.current_position = np.array(start_position)
        self.kinematics = np.array(start_kinematics)

    @property
    def _get_lat_lon_alt(self):
        return pymap3d.ecef2geodetic(*self.current_position)

    @property
    def _get_ecef_speed(self):
        return np.sqrt(sum(map(lambda x: x ** 2, self.current_position)))

    @property
    def _get_heading(self):
        lat, lon = self._get_lat_lon_alt
        return pymap3d.ecef2enu(*self.current_position, lat, lon, 0)

    def _propagate(self, timestep):
        self.last_position = self.current_position
        self.current_position += self.kinematics * timestep

    def update_position(self, timestep):
        self._propagate(timestep)
        print(self.current_position)
