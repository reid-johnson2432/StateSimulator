"""
The World class manages sim time and
keeps track of the position of all entities.
"""

from tqdm import tqdm

class World:
    def __init__(self, start_stop_time: tuple, reports, timestep=1.0, include_errors=False):
        """
        start_stop_time (2-tuple): start and end simulation time (seconds)
        reports: list of reports to capture data.
        timestep (float): Time delta between 'frames' (seconds)
        """
        start_time, stop_time = start_stop_time
        self.start_stop_range = start_stop_time
        self.current_time = start_time
        self.stop_time = stop_time
        self.timestep = timestep
        self.include_errors = include_errors

        self.entities = list()
        self.reports = reports

    def _advance_time(self):
        self.current_time += self.timestep

    def start_sim(self):
        for time in tqdm(range(*self.start_stop_range, 1), ncols=100, colour='green'):
            self.current_time = time
            for entity in self.entities:
                entity.propagator.update_position(self.current_time, self.timestep, add_error=False)
                self._update_reports(entity)
        print('Simulation Compete')

    def add_entity(self, entity):
        self.entities.append(entity)

    def _update_reports(self, entity):
        for report in self.reports:
            report.update_report(self.current_time, entity)
