import requests

import gpxpy.gpx
from datetime import timedelta
from typing import Tuple

import config


def is_acceptable_point(coord: dict) -> bool:
    """
    This methods checks if the current coordinate is not in the list of wrong
    points
    Args:
        coord (dict): contains the coordination information

    Returns:
        bool: True, if current coordinate is acceptable (not in the list of
            wrong points), otherwise False
    """
    wrong_points = config.wrong_points
    current_coord = (coord['lat'], coord['lng'])
    return not (current_coord in wrong_points)


def gpx_point(coord: dict) -> gpxpy.gpx.GPXTrackPoint:
    """
    This method is converting the the dict with the coordinates information to
    a gpxpy.gpx.GPXTrackPoint
    Args:
        coord (dict): contains the coordination information

    Returns:
        gpxpy.gpx.GPXTrackPoint: gps point, containing lat, lon, elevation and
            time
    """
    point = gpxpy.gpx.GPXTrackPoint(coord['lat'], coord['lng'])
    point.elevation = coord['alt']
    point.time = config.start_date + timedelta(seconds=coord['t'] / 1000)
    return point


def add_coords_to_track(
        tour_id: int,
        gpx_name: str,
        track: gpxpy.gpx.GPXTrack,
        auth: Tuple[str, str]) -> None:
    """
    This methods is adding all coordinates of the current segment to the track.
    Args:
        tour_id (int): id of the tour, that shall be added to the track
        gpx_name (str): name of the gpx, such that the track gets the same name
        track (gpxpy.gpx.GPXTrack): track, where the coordinates shall be added
        auth (Tuple[str, str]): login information for Komoot

    Returns:
        None
    """
    segment = gpxpy.gpx.GPXTrackSegment()
    track.segments.append(segment)
    track.name = gpx_name
    url_tour = "https://api.komoot.de/v007/tours/" + str(tour_id) + \
               "?_embedded=coordinates"
    tour_info = requests.get(url_tour, auth=auth).json()
    for coord in tour_info['_embedded']['coordinates']['items']:
        if is_acceptable_point(coord):
            segment.points.append(
                gpx_point(coord) # todo: fix bug, if multiple tracks per tour -> second track should begin where first ended
            )
    return None
