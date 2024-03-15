"""
Create a KML file to view trajectories.
"""

import simplekml


def create_trajectory_kml(trajectory_waypoints, output_path):
    """
    :param trajectory_waypoints: list of waypoints (lat, lon, alt). altitude is alt relative to ground.
    :param output_path: Location to save kml
    """
    kml = simplekml.Kml(open=1)  # the folder will be open in the table of contents
    linestring = kml.newlinestring(name="A Line")
    linestring.coords = [(lon, lat, alt) for lat, lon, alt in trajectory_waypoints]
    linestring.altitudemode = simplekml.AltitudeMode.relativetoground
    linestring.style.linestyle.color = simplekml.Color.red  # Red
    linestring.extrude = 1  # extend to ground
    # save KML to a file
    kml.save(output_path)
