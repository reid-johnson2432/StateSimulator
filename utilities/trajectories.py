"""
Functions for creating trajectories.
"""

import numpy as np

from utilities.constants import earth_radius_m
from utilities.coordinates import spherical2geodetic

g = 9.8
t_f = 120  # 2 min descent
max_alt = 1e5  # 100 km
v_f = 7e3  # velocity at impact (m/s)
v_0 = (0.5 * g * pow(t_f, 2) - max_alt) / t_f


def create_terminal_phase_trajectory(start_location: np.array, aim_point: np.array):
    phi_0, theta_0 = np.array([-1, 1]) * start_location + np.array([90, 0])
    phi_f, theta_f = np.array([-1, 1]) * aim_point + np.array([90, 0])
    dtheta_dt = (theta_f - theta_0) / t_f
    dphi_dt = (phi_f - phi_0) / t_f

    theta, phi = theta_0, phi_0
    spherical_waypoints = dict()
    for t in range(t_f + 1):
        rho = -0.5 * g * pow(t, 2) + v_0 * t + max_alt + earth_radius_m
        spherical_waypoints[t] = [rho, theta, phi]
        theta += dtheta_dt
        phi += dphi_dt

    geodetic_trajectory = {t: spherical2geodetic(*waypoint) for t, waypoint in spherical_waypoints.items()}
    return geodetic_trajectory


def create_trajectory_file(trajectory, output_filepath=None):
    df = pd.DataFrame(columns=['Time', 'Latitude', 'Longitude', 'Altitude',
                               'PosX', 'PosY', 'PosZ', 'VelX', 'VelY', 'VelZ'])
    for time, geodetic_position in trajectory.items():
        nan_array = np.empty(3)
        nan_array[:] = np.nan
        ecef_position = geodetic2ecef(*geodetic_position)
        df.loc[len(df)] = [time, *geodetic_position, *ecef_position, *nan_array]

    for idx, row in df.iterrows():
        if idx == len(df) - 1:
            break
        next_row = df.loc[idx + 1]
        next_position = np.array([next_row['PosX'], next_row['PosY'], next_row['PosZ']])
        position = np.array([row['PosX'], row['PosY'], row['PosZ']])
        delta_t = next_row['Time'] - row['Time']
        vel_x, vel_y, vel_z = (next_position - position) / delta_t
        row['VelX'] = vel_x
        row['VelY'] = vel_y
        row['VelZ'] = vel_z

    if output_filepath:
        df.to_csv(output_filepath, index=False)

    return df


if __name__ == '__main__':
    import pandas as pd
    from pymap3d.ecef import geodetic2ecef
    from metrics.visualizations.three_d_position_plot import make_3d_plot

    # shooting at white sands missile range
    peak_location, impact_wp = (36.0, -100.0), (33.2385, -106.3464)
    test_trajectory = create_terminal_phase_trajectory(peak_location, impact_wp)
    output_path = "/Users/reidjohnson/Desktop/"
    fn = 'terminal_phase'
    make_3d_plot(list(test_trajectory.values()), show=False)
    trajectory_data = create_trajectory_file(test_trajectory)
