"""
Generic Entity.
"""

import uuid

from environment.propagators.propagator import Propagator


# TODO: Use numba for properties ?


class Entity:
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', uuid.uuid4())
        propagator_class = kwargs.get('propagator_class', Propagator)
        self.propagator = propagator_class(self)
