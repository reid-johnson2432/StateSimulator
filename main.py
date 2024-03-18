"""
Start the simulation.
"""

import os

from entities.ballistic_missile import BallisticMissile
from environment.propagators.imu_propagator import IMUPropagator
from environment.propagators.trajectory_propagator import TrajectoryPropagator
from environment.world import World
from metrics.post_sim_script import post_sim_script
from reports.kinematics_report import KinematicsReport
from time import gmtime
from metrics.post_sim_script import post_set_script


def main(start_time, stop_time, seed, timestamp, propagator=TrajectoryPropagator):
    project_path = os.path.dirname(os.path.abspath(__file__))
    trajectory_filepath = os.path.join(project_path, 'external_data', 'terminal_phase.csv')

    # --- Create World ---
    reports = [KinematicsReport()]
    world = World((start_time, stop_time), reports, timestamp, post_sim_script)

    # --- Create Ballistic Missile ---
    test_missile = BallisticMissile(name='test_missile', propagator=propagator)
    test_missile.propagator.load_trajectory_file(trajectory_filepath)

    world.add_entity(test_missile)
    world.run(seed)
    set_location = world.output_location
    return set_location


if __name__ == '__main__':
    t_0 = 0
    t_f = 120
    start_seed, stop_seed = 0, 2
    realtime = gmtime()
    set_location = None
    for s in range(start_seed, stop_seed):
        print(f'Starting Seed [{s}]')
        # set_location = main(t_0, t_f, s, realtime)  # ideal trajectory
        set_location = main(t_0, t_f, s, realtime, propagator=IMUPropagator)  # Trajectory with errors

    post_set_script(set_location)
