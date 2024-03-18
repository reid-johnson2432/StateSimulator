"""
The World class manages sim time and
keeps track of the position of all entities.
"""
import os
from time import strftime

from tqdm import tqdm


class World:
    def __init__(self, start_stop_time: tuple, reports, timestamp, post_sim_script=None, timestep=1.0):
        """
        start_stop_time (2-tuple): start and end simulation time (seconds)
        reports: list of reports to capture data.
        timestep (float): Time delta between 'frames' (seconds)
        """
        self.output_location = self._make_output_location(timestamp)
        print(self.output_location)
        self.start_stop_range = start_stop_time
        self.current_time = start_stop_time[0]
        self.timestep = timestep

        self.entities = list()
        self.reports = reports
        self.post_sim_script = post_sim_script

    def run(self, seed):
        seed_output_location = os.path.join(self.output_location, str(seed))
        os.mkdir(seed_output_location)
        for time in tqdm(range(*self.start_stop_range, 1), ncols=100, colour='green'):
            self.current_time = time
            for entity in self.entities:
                self._update_reports(entity)
                entity.propagator.update_position(self.current_time, self.timestep)
        self.create_outputs(seed)

    def add_entity(self, entity):
        self.entities.append(entity)

    def _update_reports(self, entity):
        for report in self.reports:
            report.update_report(self.current_time, entity)

    def create_outputs(self, seed):
        reports = {report.__class__.__name__: report.data for report in self.reports}
        for report_name, report_data in reports.items():
            report_data.to_csv(os.path.join(self.output_location, str(seed), f'{report_name}_{seed}.csv'))
        self.post_sim_script(reports, os.path.join(self.output_location, str(seed)))

    @staticmethod
    def _make_output_location(timestamp):
        output_folder = "/Users/reidjohnson/Desktop/SimOutput"
        if not os.path.exists(output_folder):
            os.mkdir(output_folder)
        sim_name = strftime("%Y-%m-%d %H:%M:%S", timestamp).replace(' ', '-').replace(':', '')
        output_location = os.path.join(output_folder, sim_name)
        if not os.path.exists(output_location):
            os.mkdir(output_location)
        return output_location
