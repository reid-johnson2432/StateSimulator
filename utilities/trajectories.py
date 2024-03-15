"""
Functions for creating trajectories.
"""

import numpy as np

from utilities.constants import earth_radius_m
from utilities.coordinates import spherical2geodetic
from metrics.visualizations.three_d_position_plot import make_3d_plot


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
    spherical_waypoints = list()
    for t in range(t_f + 1):
        rho = -0.5 * g * pow(t, 2) + v_0 * t + max_alt + earth_radius_m
        spherical_waypoints.append([rho, theta, phi])
        theta += dtheta_dt
        phi += dphi_dt

    geodetic_trajectory = [spherical2geodetic(*waypoint) for waypoint in spherical_waypoints]
    return geodetic_trajectory


if __name__ == '__main__':
    from utilities.trajectory_to_kml import create_trajectory_kml

    # shooting at white sands missile range
    peak_location, impact_wp = (36.0, -100.0), (33.2385, -106.3464)
    test_trajectory = create_terminal_phase_trajectory(peak_location, impact_wp)
    output_path = "/Users/reidjohnson/Desktop/"
    create_trajectory_kml(test_trajectory, output_path + 'terminal_phase.kml')
    make_3d_plot(test_trajectory, show=True)
