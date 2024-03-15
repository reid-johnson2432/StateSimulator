"""
Plot trajectory lat, lon, and alt.
"""
import matplotlib.pyplot as plt


def make_3d_plot(trajectory, output_location, show=False):
    fig = plt.figure()
    fig.title = 'Test'
    ax = fig.add_subplot(projection='3d')
    xs, ys, zs, = list(zip(*trajectory))
    # trajectory
    ax.scatter(xs, ys, zs, color='red')

    ax.set_xlabel('Latitude (deg)')
    ax.set_ylabel('Longitude (deg)')
    ax.set_zlabel('Altitude (m)')

    if output_location:
        plt.savefig(output_location)
    if show:
        plt.show()
