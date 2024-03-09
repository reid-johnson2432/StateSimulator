"""
Generic Entity.
"""

import uuid

from environment.propagators.propagator import Propagator


# TODO: Use numba for properties ?


class Entity:
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', uuid.uuid4())
        self.propagator = Propagator(self)
