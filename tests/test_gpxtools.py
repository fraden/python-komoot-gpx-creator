from dotenv import load_dotenv
from mockito import when, mock, unstub, ANY
import requests
from requests.models import Response

import gpxpy

from src import gpxtools


load_dotenv()


def test_is_acceptable_point_for_not_accepptable_point():
    coord_not_acceptable = {
        "lat": 47.487856,
        "lng": 10.055955
    }
    assert not gpxtools.is_acceptable_point(coord_not_acceptable)


def test_is_acceptable_point_for_accepptable_point():
    coord_acceptable = {
            "lat": 1.2345,
            "lng": 6.7890
        }
    assert gpxtools.is_acceptable_point(coord_acceptable)


def test_add_coords_to_track():
    the_response = Response()
    the_response.status_code = 100
    the_response._content = b'{\
        "_embedded": {\
                "coordinates": {\
                    "items": [{"lat": 1, "lng": 2, "alt": 20, "t": 5},'\
                            b'{"lat": 3, "lng": 4, "alt": 30, "t": 2}]\
                }\
            }\
    }'

    when(requests).get(...).thenReturn(the_response)
    when(gpxtools).is_acceptable_point(...).thenReturn(True)

    gpx = gpxpy.gpx.GPX()
    track = gpxpy.gpx.GPXTrack()
    gpx.tracks.append(track)
    gpxtools.add_coords_to_track(1, "gpx_name", track, ("user", "pwd"))
    points = gpx.get_points_data()

    assert track.get_points_no() == 2
    assert points[0].point.latitude == 1
    assert points[0].point.longitude == 2
    assert points[0].point.elevation == 20
    assert points[1].point.latitude == 3
    assert points[1].point.longitude == 4
    assert points[1].point.elevation == 30
