"""
Geodetic Propagator.
"""

import numpy as np

from environment.propagators.propagator import Propagator
from utilities.constants import earth_radius_nm


class GeodeticPropagator(Propagator):
    def set_position(self, position: tuple, degrees=True):
        """
        :param position: (3-tuple) Latitude, Longitude, Altitude (m) of entity.
        :param degrees: (bool) Latitude and Longitude are expressed in degrees.
        """
        self.position = position

    def set_velocity(self, velocity: tuple):
        """
        :param velocity: (3-tuple) Speed (kts), Heading, and Climb Rate of entity.
        """
        self.velocity = velocity

    def update_position(self, timestep: float):
        """
        :param timestep: Amount of time (seconds) entity has been traveling.
        Computes distance traveled along great circle.
        """
        # # TODO: Handle climb rate
        lat, lon, alt = self.get_position()
        speed, heading, _ = self.get_velocity()
        dist = speed * (timestep / 3600)
        arc = dist / earth_radius_nm
        lat, lon, heading = map(np.radians, (lat, lon, heading))

        new_lat = np.arcsin(np.sin(lat) * np.cos(arc) + np.cos(lat) * np.sin(arc) * np.cos(heading))
        new_lon = lon + np.arctan2(np.sin(arc) * np.sin(heading),
                                   np.cos(lat) * np.cos(arc) - np.sin(lat) * np.sin(arc) * np.cos(heading))

        new_lat, new_lon = map(np.degrees, (new_lat, new_lon))
        self.set_position((new_lat, new_lon, alt))
        print(self.position)
