"""
Geodetic Propagator.
"""

import numpy as np
from ai.cs import cart2sp, sp2cart

from environment.propagators.trajectory_propagator import TrajectoryPropagator
from models.discrete_ins_error import get_ins_error


class IMUPropagator(TrajectoryPropagator):
    def __init__(self, entity):
        super(IMUPropagator, self).__init__(entity)
        self.attitude = np.array([0.0, 0.0, 0.0])

    def update_position(self, current_time: float, timestep: float):
        position = self.position
        current_velocity = self.velocity
        optimal_velocity = self.read_velocity(current_time)
        velo_errors = self.get_velo_errors(timestep, current_velocity, optimal_velocity)
        updated_position = position + optimal_velocity * timestep + velo_errors * timestep
        self.set_position(updated_position)
        self.set_velocity(optimal_velocity + velo_errors)

    def get_velo_errors(self, timestep, actual_velocity, optimal_velocity):
        # lat(deg), lon(deg), alt(m), vx_body(m / s), vy_body(m / s), vz_body(m / s), yaw(deg), pitch(deg), roll(deg)
        position = self.get_geo_position()

        optimal_velocity = cart2sp(*optimal_velocity)
        ini_pos_vel_att = np.array([*position, *actual_velocity, *self.attitude])
        motion_def = self._make_motion_def(ini_pos_vel_att, optimal_velocity, timestep)
        error = get_ins_error(ini_pos_vel_att, motion_def)
        velo_error_stats = error['vel']
        velo_errors = np.random.normal(np.array(velo_error_stats['avg']), np.array(velo_error_stats['std']))
        velo_errors = sp2cart(*velo_errors)
        return np.array(velo_errors)

    @staticmethod
    def _make_motion_def(ini_pos_vel_att, optimal_velocity, timestep):
        lat, lon, alt = ini_pos_vel_att[0:3]
        v_x, v_y, v_z = ini_pos_vel_att[3:6]
        yaw, pitch, roll = ini_pos_vel_att[6:9]
        motion_def = \
            f"""ini lat (deg),ini lon (deg),ini alt (m),ini vx_body (m/s),ini vy_body (m/s),ini vz_body (m/s),ini yaw (deg),ini pitch (deg),ini roll (deg)
        {lat},{lon},{alt},{v_x},{v_y},{v_z},{yaw},{pitch},{roll}
        command type,yaw (deg),pitch (deg),roll (deg),vx_body (m/s),vy_body (m/s),vz_body (m/s),command duration (s),GPS visibility
        2,0,0,0,{optimal_velocity[0]},{optimal_velocity[1]},{optimal_velocity[2]},{timestep},0
        """
        return motion_def
