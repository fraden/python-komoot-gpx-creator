import uuid
import os

import requests
import gpxpy.gpx

from helpers import *
import gpxtools
import tours_utils
import out
import config

auth = (os.getenv("KOMOOTEMAIL"), os.getenv("KOMOOTPW"))

response = requests.get(config.url_tours, auth=auth).json()
filtered_tours = tours_utils.bike_tours(response['_embedded']['tours'])

dict_tours_by_date = tours_utils.aggregate_by_date(filtered_tours)

dict_meta_data = {}
for date in dict_tours_by_date.keys():
    gpx = gpxpy.gpx.GPX()
    track = gpxpy.gpx.GPXTrack()
    gpx.tracks.append(track)

    tours = [filtered_tours[idx] for idx in dict_tours_by_date[date]]
    tours.reverse()

    gpx.name = remove_special_characters(
        tours[-1]['name'].replace('Bosch eBike Tour: ', '') + "_" + str(
            uuid.uuid4())[:8]
    )

    for tour in tours:
        gpxtools.add_coords_to_track(tour['id'], gpx.name, track, auth)

    gpx.simplify(max_distance=config.gpx_max_distance)
    gpx_txt = gpx.to_xml()

    path = os.path.join(config.output_folder, gpx.name + ".gpx")

    out.write_gpx(path, gpx_txt)

    dict_meta_data.update(
        {gpx.name: {
            "description": "",
            "rating": 5,
            "location": "Germany",
            "color": "#facc15",
            "added": "2000-01-01"

        }}
    )

out.meta_script(dict_meta_data, config.output_folder)
