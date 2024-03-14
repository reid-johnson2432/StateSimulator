"""
The World class manages sim time and
keeps track of the position of all entities.
"""

import pandas as pd


class World:
    def __init__(self, start_stop_time: tuple, timestep=60.0, include_errors=False):
        """
        start_stop_time (2-tuple): start and end simulation time (seconds)
        timestep (float): Time delta between 'frames' (seconds)
        """
        start_time, stop_time = start_stop_time
        self.current_time = start_time
        self.stop_time = stop_time
        self.timestep = timestep
        self.include_errors = include_errors

        self.entities = list()
        self.kinematics_report = pd.DataFrame(columns=['Time', 'Entity', 'PosX', 'PosY', 'PosZ', 'VelX', 'VelY', 'VelZ'])

    def _advance_time(self):
        self.current_time += self.timestep

    def start_sim(self):
        while self.stop_time > self.current_time:
            for entity in self.entities:
                entity.propagator.update_position(self.timestep, add_error=self.include_errors)
                self._update_position_report(entity)
            self._advance_time()

        print(self.kinematics_report)
        print('Simulation Compete')

    def add_entity(self, entity):
        self.entities.append(entity)

    def _update_position_report(self, entity):
        time = self.current_time
        entity_name = entity.name
        pos_x, pos_y, pos_z = entity.propagator.get_position()
        vel_x, vel_y, vel_z = entity.propagator.get_velocity(add_error=False)
        row_data = [time, entity_name, pos_x, pos_y, pos_z, vel_x, vel_y, vel_z]
        index = len(self.kinematics_report)
        self.kinematics_report.loc[index] = row_data
