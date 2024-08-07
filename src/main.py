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

#dict_tours_by_date = {datetime.date(2023, 6, 24): dict_tours_by_date[datetime.date(2023, 6, 24)]}

dict_meta_data = {}
for date in dict_tours_by_date.keys():
    gpx = gpxpy.gpx.GPX()
    track = gpxpy.gpx.GPXTrack()
    gpx.tracks.append(track)

    tours = [filtered_tours[idx] for idx in dict_tours_by_date[date]]
    tours.reverse()
    if os.getenv('SHOW_REAL_DATES'):
        date_in_metadata = str(date)
        postfix = date_in_metadata
    else:
        date_in_metadata = "2000-01-01"
        postfix = str(uuid.uuid4())[:8]


    gpx.name = remove_special_characters(
        tours[-1]['name'].replace('Bosch eBike Tour: ', '') + "_" + postfix
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
            "added": date_in_metadata

        }}
    )

if os.getenv('SHOW_REAL_DATES'):
    out.meta_script(dict_meta_data, config.output_folder)
