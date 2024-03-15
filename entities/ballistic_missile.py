"""
Maritime Object.
"""

from entities.entity import Entity
from environment.propagators.trajectory_propagator import TrajectoryPropagator


class BallisticMissile(Entity):
    def __init__(self, **kwargs):
        super(BallisticMissile, self).__init__(**kwargs)
        self.propagator = TrajectoryPropagator(self)
