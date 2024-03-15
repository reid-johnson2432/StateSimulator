"""
Maritime Object.
"""

from entities.entity import Entity
from environment.propagators.trajectory_propagator import TrajectoryPropagator


class BallisticMissile(Entity):
    def __init__(self, propagator=TrajectoryPropagator, **kwargs):
        super(BallisticMissile, self).__init__(**kwargs)
        self.propagator = propagator(self)
