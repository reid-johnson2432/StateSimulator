"""
Convert Spherical coordinates to geodetic.
"""

from utilities.constants import earth_radius_m


def spherical2geodetic(rho, theta, phi, deg=True):
    """
    :param rho:
    :param theta:
    :param phi:
    :param deg: True if theta and phi are provided in degrees.
    :return:
    """

    lat, lon, alt = 90 - phi, theta, rho - earth_radius_m
    return lat, lon, alt
