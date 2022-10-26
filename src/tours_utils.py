from datetime import datetime

from typing import List

import config


def bike_tours(tours: List[dict]) -> List[dict]:
    """
    This method filters the tours, such that only done bike tours are
    remaining.
    Args:
        tours (List[dict]): tours, that shall be filtered

    Returns:
        List[dict]: filtered bike tours
    """
    relevant_keys = config.relevant_keys

    tours_filtered = [
        {key: tour[key] for key in relevant_keys if key in tour.keys()} for
        tour in tours]
    tours_filtered = [tour for tour in tours_filtered if
                      not (tour['type'] != 'tour_recorded' or tour[
                          'sport'] != 'touringbicycle')]
    return tours_filtered


def aggregate_by_date(tours: List[dict]) -> dict:
    """
    This method is aggregating the tours by date.
    Args:
        tours (List[dict]): tours with meta information, like date and id

    Returns:
        dict: aggregated tours
    """
    dict_output_dates = dict()
    for idx, tour in enumerate(tours):
        date = datetime.strptime(tour['date'], "%Y-%m-%dT%H:%M:%S.%f%z").date()
        if date in dict_output_dates:
            dict_output_dates[date].append(idx)
        else:
            dict_output_dates[date] = [idx]
    return dict_output_dates
