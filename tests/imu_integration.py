"""
Start the simulation.
"""

import numpy as np

from entities.entity import Entity
from environment.propagators.ecef_propagator import ECEFPropagator
from environment.world import World
from utilities.constants import earth_radius_nm, m_per_nm


def main(start_time, stop_time):
    world = World((start_time, stop_time), include_errors=False)
    # Test Case: Start at (0, 0) lat, lon on surface. Travel due north at 1 kts for 1 hour
    start_position = np.array([1.0, 1.0, 0.0]) * earth_radius_nm * m_per_nm
    start_velocity = (0.0, 1.0, 0.0)
    test_missile = Entity(name='TestMissile', propagator_class=ECEFPropagator)
    test_missile.propagator.set_position(tuple(start_position))
    test_missile.propagator.set_velocity(start_velocity)
    world.add_entity(test_missile)
    world.start_sim()


if __name__ == '__main__':
    t_0 = 0.0
    t_f = 3600.0
    main(t_0, t_f)

# (6371460.205646288, 6370879.994536818, -0.09331996578205122)
