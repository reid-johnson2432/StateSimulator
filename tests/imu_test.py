# -*- coding: utf-8 -*-
# Filename: demo_free_integration.py

import math
import os

import numpy as np

from gnss_ins_sim.sim import ins_sim
from models.aceinna_imu_381 import get_imu381_model

# globals
D2R = math.pi / 180

fs = 100.0  # IMU sample frequency


# TODO: Repeatability problem ?
def main(ini_pos_vel_att, motion_def):
    """
    param ini_pos_vel_att: numpy array:
      lat (deg), lon (deg), alt (m), vx_body (m/s), vy_body (m/s), vz_body (m/s), yaw (deg), pitch (deg), roll (deg)
    param motion_def: csv-type:

    return:
    """
    imu = get_imu381_model()
    # --- Algorithm
    # Free integration in a virtual inertial frame
    from demo_algorithms import free_integration_odo
    ini_pos_vel_att[0] = ini_pos_vel_att[0] * D2R
    ini_pos_vel_att[1] = ini_pos_vel_att[1] * D2R
    ini_pos_vel_att[6:9] = ini_pos_vel_att[6:9] * D2R
    # add initial states error if needed
    ini_vel_err = np.array([0.0, 0.0, 0.0])  # initial velocity error in the body frame, m/s
    ini_att_err = np.array([0.0, 0.0, 0.0])  # initial Euler angles error, deg
    ini_pos_vel_att[3:6] += ini_vel_err
    ini_pos_vel_att[6:9] += ini_att_err * D2R
    # create the algorith object
    algo1 = free_integration_odo.FreeIntegration(ini_pos_vel_att)

    # --- start simulation ---
    sim = ins_sim.Sim([fs, 0.0, 0.0],
                      motion_def,
                      ref_frame=1,
                      imu=imu,
                      mode=None,
                      env=None,
                      algorithm=algo1)
    # run the simulation for 1000 times
    sim.run(1)
    # generate simulation results, summary
    # do not save data since the simulation runs for 1000 times and generates too many results
    # sim.results(err_stats_start=-1, gen_kml=True)
    # plot postion error
    sim.plot(['pos'], opt={'pos': 'error'})
    interested_errors = ['pos', 'vel']
    stats_fields = ['max', 'avg', 'std']

    errors_dict = dict()
    for error_type in interested_errors:
        errors_dict[error_type] = dict()
        error_stats = sim.dmgr.get_error_stats(error_type)
        for stat_field in stats_fields:
            errors_dict[error_type][stat_field] = error_stats[stat_field]['algo0_0']
    return errors_dict


if __name__ == '__main__':
    project_directory = os.path.abspath(__file__).split('tests')[0]
    motion_def_path = os.path.join(project_directory, 'gnss-ins-sim/demo_motion_def_files/motion_def-90deg_turn.csv')
    initial_position = [31.9965, 120.004, 0]
    initial_velocity = [10, 0, 0]
    initial_att = [315, 0, 0]
    errors = main(np.array(initial_position + initial_velocity + initial_att), motion_def_path)
    steve = 1
