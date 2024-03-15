"""
Propagators are used to
manage entity locations.
"""

import numpy as np
import pandas as pd

from environment.propagators.propagator import Propagator


class TrajectoryPropagator(Propagator):
    def __init__(self, entity, **kwargs):
        super(TrajectoryPropagator, self).__init__(entity, **kwargs)
        self.trajectory_data = None

    def update_position(self, current_time: float, timestep: float, **kwargs):
        position = self.position
        optimal_velocity = self.read_velocity(current_time)
        if kwargs.get('add_errors', False):
            pass
        updated_position = position + optimal_velocity * timestep
        self.set_position(updated_position)

    def load_trajectory_file(self, filepath):
        self.trajectory_data = pd.read_csv(filepath)
        self.trajectory_data.set_index('Time')
        min_time = self.trajectory_data['Time'].min()
        trajectory_now = self.trajectory_data[self.trajectory_data['Time'] == min_time]
        pos_x, pos_y, pos_z = trajectory_now['PosX'].values[0], trajectory_now['PosY'].values[0], \
                              trajectory_now['PosZ'].values[0]
        vel_x, vel_y, vel_z = trajectory_now['VelX'].values[0], trajectory_now['VelY'].values[0], \
                              trajectory_now['VelZ'].values[0]

        self.set_position(np.array([pos_x, pos_y, pos_z]))
        self.set_velocity(np.array([vel_x, vel_y, vel_z]))

    def read_position(self, current_time):
        trajectory_now = self.trajectory_data[self.trajectory_data['Time'] == current_time]
        pos_x, pos_y, pos_z = trajectory_now['PosX'].values[0], trajectory_now['PosY'].values[0], \
                              trajectory_now['PosZ'].values[0]
        return np.array([pos_x, pos_y, pos_z])

    def read_velocity(self, current_time):
        trajectory_now = self.trajectory_data[self.trajectory_data['Time'] == current_time]
        vel_x, vel_y, vel_z = trajectory_now['VelX'].values[0], trajectory_now['VelY'].values[0], \
                              trajectory_now['VelZ'].values[0]
        return np.array([vel_x, vel_y, vel_z])


if __name__ == '__main__':
    from entities.ballistic_missile import BallisticMissile

    start_time, stop_time = 0, 120
    # --- Create Ballistic Missile ---
    test_missile = BallisticMissile(name='test_missile')

    trajectory_filepath = "/Users/reidjohnson/Desktop/terminal_phase.csv"
    test_missile.propagator.load_trajectory_file(trajectory_filepath)
    ts = 1
    for time in range(start_time, stop_time + 1, ts):
        pos = test_missile.propagator.get_geo_position()
        velo = test_missile.propagator.velocity
        test_missile.propagator.update_position(time, ts)
        print(f'time: {time} \n position: {pos} \n velocity: {velo} \n\n')
