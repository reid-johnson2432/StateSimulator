"""
Functions for creating trajectories.
"""

from pymap3d.vincenty import track2, vdist


def create_parabolic_trajectory(launch_point, aim_point, peak_alt, launch_time, num_waypoints=100):
    total_dist = vdist(*launch_point, *aim_point)[0]
    x_intercept_l, x_intercept_r = 0, total_dist
    peak_waypoint = (total_dist / 2.0, peak_alt)
    a_coefficient = peak_waypoint[1] / (peak_waypoint[0] - x_intercept_l) * (peak_waypoint[0] - x_intercept_r)

    gc_track = list(zip(*track2(*launch_point, *aim_point, npts=num_waypoints)))
    trajectory = dict()
    time = launch_time
    for lat, lon in gc_track:
        ground_range = vdist(*launch_point, lat, lon)[0]
        alt = a_coefficient * (ground_range - x_intercept_l) * (ground_range - x_intercept_r)
        trajectory[time] = [lat, lon, alt]
        # TODO: Use weapon speed to determine time
        time += 1

    return trajectory
