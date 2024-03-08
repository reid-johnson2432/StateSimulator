"""
Start the simulation.
"""

from world import World
from entities.generic_entity import GenericEntity
from utilities.constants import earth_radius_m, kts_to_ms


def main(start_time, stop_time, **kwargs):
    world = World((start_time, stop_time))

    # Test Case: Start at (0, 0) lat, lon on surface. Travel due north at 60 kts for 1 hour
    # start_position = (earth_radius_m, earth_radius_m, 0)
    # start_velocity = (0, 0, 60 * kts_to_ms)
    start_position = (0.0, 0.0, 0.0)
    start_velocity = (1.0, 1.0, 1.0)
    test_entity = GenericEntity(start_position, start_velocity)
    world.register_entity(test_entity)
    world.start_sim()


if __name__ == '__main__':
    t_0 = 0.0
    t_f = 3600.0
    main(t_0, t_f)
