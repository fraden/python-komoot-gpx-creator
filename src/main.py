import requests
import os
from datetime import datetime, timedelta

import gpxpy.gpx
import uuid

from helpers import meta_script, is_wrong_point, filter_tours
import config

output_folder = config.output_folder

url = "https://api.komoot.de/v007/users/" + os.getenv(
    "USERID") + "/tours/?page=0&limit=1000"
auth = (os.getenv("KOMOOTEMAIL"), os.getenv("KOMOOTPW"))
r = requests.get(url, auth=auth)

response = r.json()
tours_filtered = filter_tours(response['_embedded']['tours'])

dict_output_dates = dict()
for idx, tour in enumerate(tours_filtered):
    if tour['type'] != 'tour_recorded' and tour['sport'] != 'touringbicycle':
        continue
    date = datetime.strptime(tour['date'], "%Y-%m-%dT%H:%M:%S.%f%z").date()
    if date in dict_output_dates:
        dict_output_dates[date].append(idx)
    else:
        dict_output_dates[date] = [idx]

dict_output_dates_items = list(dict_output_dates.keys())
dict_output_dates_items.reverse()

dict_output = {}
for date in dict_output_dates_items:
    trips_on_day = len(dict_output_dates[date])
    gpx = gpxpy.gpx.GPX()
    track = gpxpy.gpx.GPXTrack()
    gpx.tracks.append(track)
    track.name = gpx.name
    if trips_on_day > 1:

        tours = [tours_filtered[idx] for idx in dict_output_dates[date]]

        tours.reverse()
        gpx.name = tours[-1]['name'] + "_" + str(uuid.uuid4())[:8]

        start_date = datetime.strptime("2000-01-01T00:00:00.000Z",
                                       "%Y-%m-%dT%H:%M:%S.%f%z")

        for tour in tours:
            segment = gpxpy.gpx.GPXTrackSegment()
            track.segments.append(segment)
            track.name = gpx.name
            url_tour = "https://api.komoot.de/v007/tours/" + str(
                tour['id']) + "?_embedded=coordinates"
            tour_infos = requests.get(url_tour, auth=auth).json()
            for coord in tour_infos['_embedded']['coordinates']['items']:
                if is_wrong_point(coord):
                    continue
                point = gpxpy.gpx.GPXTrackPoint(coord['lat'], coord['lng'])
                point.elevation = coord['alt']
                point.time = start_date + timedelta(seconds=coord['t'] / 1000)
                segment.points.append(point)
    else:
        tour = tours_filtered[dict_output_dates[date][0]]

        segment = gpxpy.gpx.GPXTrackSegment()
        track.segments.append(segment)
        gpx.name = tour['name'] + "_" + str(uuid.uuid4())[:8]
        track.name = gpx.name
        url_tour = "https://api.komoot.de/v007/tours/" + str(
            tour['id']) + "?_embedded=coordinates"
        tour_infos = requests.get(url_tour, auth=auth).json()

        start_date = datetime.strptime("2000-01-01T00:00:00.000Z",
                                       "%Y-%m-%dT%H:%M:%S.%f%z")
        for coord in tour_infos['_embedded']['coordinates']['items']:
            if is_wrong_point(coord):
                continue
            point = gpxpy.gpx.GPXTrackPoint(coord['lat'], coord['lng'])
            point.elevation = coord['alt']
            point.time = start_date + timedelta(seconds=coord['t'] / 1000)
            segment.points.append(point)

    gpx_txt = gpx.to_xml()
    gpx_replaced_name = gpx.name.replace(".", "_").replace(":", "_").replace(
        " ", "_").replace("-", "_").replace("–",
                                            "_").replace(
        "(", "_").replace(")", "_").replace("ä", "ae").replace("ö",
                                                               "oe").replace(
        "ü", "ue")

    path = os.path.join(os.path.realpath('..'), output_folder,
                        gpx_replaced_name + ".gpx")
    f = open(path, 'w', encoding="utf-8")

    g = gpxpy.parse(gpx_txt)
    g.simplify(max_distance=10)
    gpx_txt = g.to_xml()

    f.write(gpx_txt)
    f.close()
    dict_output.update(
        {gpx_replaced_name: {
            "description": "",
            "rating": 5,
            "location": "Germany",
            "color": "#facc15",
            "added": "2000-01-01"

        }}
    )

meta_script(dict_output, output_folder)