"""
The World class manages sim time and
keeps track of the position of all entities.
"""
import os.path

from tqdm import tqdm
from time import gmtime, strftime


class World:
    def __init__(self, start_stop_time: tuple, reports, post_sim_script=None, timestep=1.0, include_errors=False):
        """
        start_stop_time (2-tuple): start and end simulation time (seconds)
        reports: list of reports to capture data.
        timestep (float): Time delta between 'frames' (seconds)
        """
        self.output_location = self._make_output_location()
        self.start_stop_range = start_stop_time
        self.current_time = start_stop_time[0]
        self.timestep = timestep
        self.include_errors = include_errors

        self.entities = list()
        self.reports = reports
        self.post_sim_script = post_sim_script

    def run(self):
        for time in tqdm(range(*self.start_stop_range, 1), ncols=100, colour='green'):
            self.current_time = time
            for entity in self.entities:
                entity.propagator.update_position(self.current_time, self.timestep)
                self._update_reports(entity)
        self.end_sim()

    def add_entity(self, entity):
        self.entities.append(entity)

    def _update_reports(self, entity):
        for report in self.reports:
            report.update_report(self.current_time, entity)

    def end_sim(self):
        print('Creating Output')
        reports = {report.__class__.__name__: report.data for report in self.reports}
        for report_name, report_data in reports.items():
            report_data.to_csv(os.path.join(self.output_location, f'{report_name}.csv'))
        self.post_sim_script(reports, self.output_location)
        print('Outputs Created')

    @staticmethod
    def _make_output_location():
        output_folder = "/Users/reidjohnson/Desktop/SimOutput"
        if not os.path.exists(output_folder):
            os.mkdir(output_folder)
        sim_name = strftime("%Y-%m-%d %H:%M:%S", gmtime()).replace(' ', '-').replace(':', '')
        output_location = os.path.join(output_folder, sim_name)
        os.mkdir(output_location)
        return output_location
