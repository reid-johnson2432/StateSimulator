"""
Geodetic Propagator.
"""

import numpy as np

from environment.propagators.propagator import Propagator
from models.discrete_ins_error import get_ins_error
from pymap3d.ecef import ecef2geodetic


class ECEFPropagator(Propagator):
    def __init__(self, entity):
        super(ECEFPropagator, self).__init__(entity)
        self.attitude = tuple([0.0, 0.0, 0.0])

    def set_position(self, position: tuple):
        """
        :param position: (3-tuple) PosX, PosY, PosZ (m) of entity.
        """
        self.position = position

    def set_velocity(self, velocity: tuple):
        """
        :param velocity: (3-tuple) vel_x, vel_y, vel_z (m/s) of entity.
        """
        self.velocity = velocity

    def update_position(self, timestep: float, **kwargs):
        """
        :param timestep: Amount of time (seconds) entity has been traveling.
        Computes distance traveled along great circle.
        """
        # # TODO: Handle climb rate
        pos_x, pos_y, pos_z = self.get_position()
        add_error = kwargs.get('add_error', False)
        vel_x, vel_y, vel_z = self.get_velocity(add_error=add_error)

        new_pos_x, new_pos_y, new_pos_z = np.array([pos_x, pos_y, pos_z]) + np.array([vel_x, vel_y, vel_z]) * timestep
        self.set_position((new_pos_x, new_pos_y, new_pos_z))
        print(self.position)

    def add_error(self, timestep):
        """
        :param timestep:
        :return: Does not return, adds error to velocity
        """
        # lat(deg), lon(deg), alt(m), vx_body(m / s), vy_body(m / s), vz_body(m / s), yaw(deg), pitch(deg), roll(deg)
        position = self.get_position()
        geodetic_pos = ecef2geodetic(*position)
        velocity = self.velocity
        attitude = self.attitude

        ini_pos_vel_att = np.array([*geodetic_pos, *velocity, *attitude])
        motion_def = self._make_motion_def(ini_pos_vel_att, timestep)
        error = get_ins_error(ini_pos_vel_att, motion_def)
        velo_error_stats = error['vel']
        velo_errors = np.random.normal(np.array(velo_error_stats['avg']), np.array(velo_error_stats['std']))
        velocity = tuple(np.array(velocity) + velo_errors)
        self.set_velocity(velocity)

    def get_velocity(self, add_error=False):
        if add_error:
            timestep = 60.0  # TODO: remove hardcoded timestep
            self.add_error(timestep)
        return self.velocity

    @staticmethod
    def _make_motion_def(ini_pos_vel_att, timestep):
        lat, lon, alt = ini_pos_vel_att[0:3]
        v_x, v_y, v_z = ini_pos_vel_att[3:6]
        yaw, pitch, roll = ini_pos_vel_att[6:9]
        motion_def = \
        f"""ini lat (deg),ini lon (deg),ini alt (m),ini vx_body (m/s),ini vy_body (m/s),ini vz_body (m/s),ini yaw (deg),ini pitch (deg),ini roll (deg)
        {lat},{lon},{alt},{v_x},{v_y},{v_z},{yaw},{pitch},{roll}
        command type,yaw (deg),pitch (deg),roll (deg),vx_body (m/s),vy_body (m/s),vz_body (m/s),command duration (s),GPS visibility
        1,0,0,0,0,0,0,{timestep},0
        """
        return motion_def