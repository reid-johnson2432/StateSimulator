"""
Start the simulation.
"""

from entities.ballistic_missile import BallisticMissile
from environment.world import World
from reports.kinematics_report import KinematicsReport


def main(start_time, stop_time):
    # --- Create World ---
    reports = [KinematicsReport()]
    world = World((start_time, stop_time), reports)

    # --- Create Ballistic Missile ---
    test_missile = BallisticMissile(name='test_missile')

    trajectory_filepath = "/Users/reidjohnson/Desktop/terminal_phase.csv"
    test_missile.propagator.load_trajectory_file(trajectory_filepath)

    world.add_entity(test_missile)
    world.start_sim()


if __name__ == '__main__':
    t_0 = 0
    t_f = 120
    main(t_0, t_f)
