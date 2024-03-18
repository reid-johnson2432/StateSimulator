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


def main(start_time, stop_time, propagator=TrajectoryPropagator):
    project_path = os.path.dirname(os.path.abspath(__file__))
    # --- Create World ---
    reports = [KinematicsReport()]
    world = World((start_time, stop_time), reports, post_sim_script)

    # --- Create Ballistic Missile ---
    test_missile = BallisticMissile(name='test_missile', propagator=propagator)

    trajectory_filepath = os.path.join(project_path, 'external_data', 'terminal_phase.csv')
    test_missile.propagator.load_trajectory_file(trajectory_filepath)

    world.add_entity(test_missile)
    start_seed, stop_seed = 0, 1
    world.run(start_seed, stop_seed)


if __name__ == '__main__':
    t_0 = 0
    t_f = 120

    main(t_0, t_f)  # ideal trajectory
    # main(t_0, t_f, propagator=IMUPropagator)  # Trajectory with errors
