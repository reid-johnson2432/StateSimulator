"""
Propagators are used to
manage entity locations.
"""


class Propagator:
    def __init__(self, entity):
        """
        Abstract class to manage entity kinematics.
        :param entity: Platform in simulation.
        """
        self.entity = entity
        self.position = None
        self.velocity = None

    def get_position(self):
        return self.position

    def get_velocity(self):
        return self.velocity

    def set_position(self, position: tuple):
        raise NotImplementedError

    def set_velocity(self, velocity: tuple):
        raise NotImplementedError

    def update_position(self, timestep: float, **kwargs):
        raise NotImplementedError
