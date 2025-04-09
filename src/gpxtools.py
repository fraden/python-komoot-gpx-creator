import requests
import os

import gpxpy.gpx
from datetime import timedelta, datetime
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


def gpx_point(coord: dict,
              start_date: datetime.strptime) -> \
        gpxpy.gpx.GPXTrackPoint:
    """
    This method is converting the the dict with the coordinates information to
    a gpxpy.gpx.GPXTrackPoint
    Args:
        coord (dict): contains the coordination information
        start_date (datetime.strptime)

    Returns:
        gpxpy.gpx.GPXTrackPoint: gps point, containing lat, lon, elevation and
            time
    """
    point = gpxpy.gpx.GPXTrackPoint(coord['lat'], coord['lng'])
    point.elevation = coord['alt']
    point.time = start_date + timedelta(seconds=coord['t'] / 1000)
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
    if os.getenv('SHOW_REAL_DATES') == '1':
        start_date = datetime.strptime(tour_info['date'],
                               "%Y-%m-%dT%H:%M:%S.%f%z")
    else:
        start_date = config.start_date
    for coord in tour_info['_embedded']['coordinates']['items']:
        if is_acceptable_point(coord):
            segment.points.append(
                gpx_point(coord, start_date=start_date)
            )
    return None
