"""
Maritime Object.
"""

from entities.entity import Entity
from environment.propagators.geodetic_propagator import GeodeticPropagator


class MaritimeObject(Entity):
    def __init__(self, **kwargs):
        super(MaritimeObject, self).__init__(**kwargs)
        self.propagator = GeodeticPropagator(self)
