"""
Start the simulation.
"""

import os
from entities.ballistic_missile import BallisticMissile
from environment.world import World
from reports.kinematics_report import KinematicsReport
from metrics.post_sim_script import post_sim_script


def main(start_time, stop_time):
    project_path = os.path.dirname(os.path.abspath(__file__))
    # --- Create World ---
    reports = [KinematicsReport()]
    world = World((start_time, stop_time), reports, post_sim_script)

    # --- Create Ballistic Missile ---
    test_missile = BallisticMissile(name='test_missile')

    trajectory_filepath = os.path.join(project_path, 'external_data', 'terminal_phase.csv')
    test_missile.propagator.load_trajectory_file(trajectory_filepath)

    world.add_entity(test_missile)
    world.run()


if __name__ == '__main__':
    t_0 = 0
    t_f = 120
    output_location = "/Users/reidjohnson/Desktop/SimOutput"
    main(t_0, t_f)
