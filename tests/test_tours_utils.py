import datetime

from src import tours_utils


def test_bike_tours_for_irrelevant_keys():
    tours = [
        {'date': '2020-01-01T18:07:18.000Z', 'irrelevant_key_0': "bla",
         'name': 'Bosch eBike Tour: Heilbronn', 'sport': 'touringbicycle',
         'source': '{"api":"de.komoot.main-api/tour/import",\
         "type":"tour_recorded","id":123456}',
         'distance': 38494.0, 'duration': 7121, 'elevation_up': 720.0,
         'elevation_down': 724.0, 'time_in_motion': 6501, 'id': 123456,
         'type': 'tour_recorded'},
        {'date': '2020-01-01T16:04:55.000Z',
         'name': 'Bosch eBike Tour: Muenchen', 'sport': 'touringbicycle',
         'source': '{"api":"de.komoot.main-api/tour/import",\
         "type":"tour_recorded","id":1234567}',
         'distance': 22113.0, 'duration': 6197, 'elevation_up': 836.0,
         'elevation_down': 834.0, 'time_in_motion': 4710, 'id': 1234567,
         'type': 'tour_recorded', 'irrelevant_key_1': 2.3},
        {'date': '2020-01-01T19:00:53.000Z',
         'name': 'Bosch eBike Tour: Stuttgart', 'sport': 'touringbicycle',
         'source': '{"api":"de.komoot.main-api/tour/import",\
         "type":"tour_recorded","id":12345678}',
         'distance': 2682.0, 'duration': 505, 'elevation_up': 44.0,
         'elevation_down': 25.0, 'time_in_motion': 468, 'id': 12345678,
         'type': 'tour_recorded', 'irrelevant_key_2': 2}]

    tours = tours_utils.bike_tours(tours)
    assert 'irrelevant_key_0' not in tours[0].keys()
    assert 'irrelevant_key_1' not in tours[0].keys()
    assert 'irrelevant_key_2' not in tours[0].keys()


def test_bike_tours_for_irrelevant_tour_type():
    tours = [
        {'date': '2020-01-01T18:07:18.000Z', 'irrelevant_key_0': "bla",
         'name': 'Bosch eBike Tour: Heilbronn', 'sport': 'touringbicycle',
         'source': '{"api":"de.komoot.main-api/tour/import",\
         "type":"tour_not_recorded","id":123456}',
         'distance': 38494.0, 'duration': 7121, 'elevation_up': 720.0,
         'elevation_down': 724.0, 'time_in_motion': 6501, 'id': 123456,
         'type': 'tour_not_recorded'},
        {'date': '2020-01-01T16:04:55.000Z',
         'name': 'Bosch eBike Tour: Muenchen', 'sport': 'touringbicycle',
         'source': '{"api":"de.komoot.main-api/tour/import",\
         "type":"tour_recorded","id":1234567}',
         'distance': 22113.0, 'duration': 6197, 'elevation_up': 836.0,
         'elevation_down': 834.0, 'time_in_motion': 4710, 'id': 1234567,
         'type': 'tour_recorded', 'irrelevant_key_1': 2.3},
        {'date': '2020-01-01T19:00:53.000Z',
         'name': 'Bosch eBike Tour: Stuttgart', 'sport': 'touringbicycle',
         'source': '{"api":"de.komoot.main-api/tour/import",\
         "type":"tour_not_recorded","id":12345678}',
         'distance': 2682.0, 'duration': 505, 'elevation_up': 44.0,
         'elevation_down': 25.0, 'time_in_motion': 468, 'id': 12345678,
         'type': 'tour_not_recorded', 'irrelevant_key_2': 2}]

    tours = tours_utils.bike_tours(tours)
    assert len(tours) == 1
    assert tours[0]['name'] == 'Bosch eBike Tour: Muenchen'


def test_bike_tours_for_irrelevant_tour_sport():
    tours = [
        {'date': '2020-01-01T18:07:18.000Z', 'irrelevant_key_0': "bla",
         'name': 'Bosch eBike Tour: Heilbronn', 'sport': 'walking',
         'source': '{"api":"de.komoot.main-api/tour/import",\
         "type":"tour_recorded","id":123456}',
         'distance': 38494.0, 'duration': 7121, 'elevation_up': 720.0,
         'elevation_down': 724.0, 'time_in_motion': 6501, 'id': 123456,
         'type': 'tour_recorded'},
        {'date': '2020-01-01T16:04:55.000Z',
         'name': 'Bosch eBike Tour: Muenchen', 'sport': 'touringbicycle',
         'source': '{"api":"de.komoot.main-api/tour/import",\
         "type":"tour_recorded","id":1234567}',
         'distance': 22113.0, 'duration': 6197, 'elevation_up': 836.0,
         'elevation_down': 834.0, 'time_in_motion': 4710, 'id': 1234567,
         'type': 'tour_recorded', 'irrelevant_key_1': 2.3},
        {'date': '2020-01-01T19:00:53.000Z',
         'name': 'Bosch eBike Tour: Stuttgart', 'sport': 'touringbicycle',
         'source': '{"api":"de.komoot.main-api/tour/import",\
         "type":"tour_recorded","id":12345678}',
         'distance': 2682.0, 'duration': 505, 'elevation_up': 44.0,
         'elevation_down': 25.0, 'time_in_motion': 468, 'id': 12345678,
         'type': 'tour_recorded', 'irrelevant_key_2': 2}]

    tours = tours_utils.bike_tours(tours)
    assert len(tours) == 2
    assert tours[0]['name'] == 'Bosch eBike Tour: Muenchen'
    assert tours[1]['name'] == 'Bosch eBike Tour: Stuttgart'


def test_aggregate_by_date():
    tours = [
        {
            'date': '2020-01-01T18:07:18.000Z',
            'name': 'Bosch eBike Tour: Stuttgart', 'sport': 'touringbicycle',
            'source': '{"api":"de.komoot.main-api/tour/import",\
            "type":"tour_recorded","id":1234}',
            'distance': 38494.0, 'duration': 7121, 'elevation_up': 720.0,
            'elevation_down': 724.0, 'time_in_motion': 6501, 'id': 1234,
            'type': 'tour_recorded'
        },
        {
            'date': '2020-01-02T16:04:55.000Z',
            'name': 'Bosch eBike Tour: Muenchen',
            'sport': 'touringbicycle',
            'source': '{"api":"de.komoot.main-api/tour/import",\
            "type":"tour_recorded","id":12345}',
            'distance': 22113.0, 'duration': 6197,
            'elevation_up': 836.0,
            'elevation_down': 834.0,
            'time_in_motion': 4710, 'id': 12345,
            'type': 'tour_recorded'
        },
        {
            'date': '2020-01-02T19:34:53.000Z',
            'name': 'Bosch eBike Tour: Muenchen', 'sport': 'touringbicycle',
            'source': '{"api":"de.komoot.main-api/tour/import",\
            "type":"tour_recorded","id":123456}',
            'distance': 2682.0, 'duration': 505, 'elevation_up': 44.0,
            'elevation_down': 25.0, 'time_in_motion': 468, 'id': 123456,
            'type': 'tour_recorded'
        }
    ]

    dict_tours_by_date = tours_utils.aggregate_by_date(tours)

    date_1 = datetime.date(2020, 1, 1)
    date_2 = datetime.date(2020, 1, 2)
    assert len(dict_tours_by_date.keys()) == 2
    assert dict_tours_by_date[date_1] == [0]
    assert dict_tours_by_date[date_2] == [1, 2]
