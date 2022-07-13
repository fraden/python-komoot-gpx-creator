import os
from datetime import datetime

output_folder = "out"
relevant_keys = ['date', 'name', 'sport', 'source', 'distance', 'duration',
                 'elevation_up', 'elevation_down',
                 'time_in_motion', 'id', 'type']
start_date = datetime.strptime("2000-01-01T00:00:00.000Z",
                               "%Y-%m-%dT%H:%M:%S.%f%z")
gpx_max_distance = 10

url_tours = "https://api.komoot.de/v007/users/" + os.getenv(
    "USERID") + "/tours/?page=0&limit=1000"

wrong_points = [(47.487856, 10.055955), (47.516115, 10.419015)]
