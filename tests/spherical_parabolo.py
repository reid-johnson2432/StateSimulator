"""
Create a parabola in spherical coordinates.
"""

import numpy as np
from utilities.constants import earth_radius_nm, m_per_nm

g = -9.8
v_0 = np.pi * 10
h_0 = earth_radius_nm * m_per_nm
phi_0 = np.pi / 6


def rho(time):
    """
    meteres
    :param time:
    :return:
    """
    return -0.5 * pow(time, 2) + v_0 * time + h_0


def theta(time):
    """
    radians
    :param time:
    :return:
    """
    return v_0 / (earth_radius_nm * m_per_nm) * time


def phi(time):
    """
    radians
    :param time:
    :return:
    """
    return 0


def parameterize_parabola():
    positions = list()
    for t in range(100):
        pos_t = [rho(t), theta(t), phi(t)]
        positions.append(pos_t)
    return positions


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import numpy as np

    from ai import cs

    spherical_positions = parameterize_parabola()
    cartesian_positions = [list(cs.sp2cart(*pos)) for pos in spherical_positions]
    # plot a 3D surface like in the example mplot3d/surface3d_demo
    X = list()
    Y = list()
    Z = list()
    for pos in cartesian_positions:
        X.append(pos[0])
        Y.append(pos[1])
        Z.append(pos[2])

    plt.plot(X, Z)

    plt.show()
