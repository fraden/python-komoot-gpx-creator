import random
import os
import re
from datetime import datetime

import numpy as np

import config


def random_color():
    return "#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])


def meta_script(dict_of_trips, output_folder):
    metajs = "const colors = require('tailwindcss/colors') " \
             "// eslint-disable-line \nconst meta ={\n"
    for key in dict_of_trips:
        print(key)
        metajs = metajs + key + ": {\ndescription:\n'" + dict_of_trips[key][
            'description'] + "',\nrating:5,\nlocation: 'Germany', color:'" \
            + random_color() + "',\nadded:'2020-01-01'},"

    metajs = metajs + "}\nmodule.exports = { meta }"
    f = open(os.path.join(os.path.realpath('..'), output_folder, "meta.js"),
             'w', encoding="utf-8")
    f.write(metajs)
    f.close()


def is_wrong_point(coord):
    wrong_points = [(47.487856, 10.055955), (47.516115, 10.419015)]
    current_coord = (coord['lat'], coord['lng'])
    return current_coord in wrong_points


def filter_tours(tours):
    relevant_keys = config.relevant_keys

    tours_filtered = [
        {key: tour[key] for key in relevant_keys if key in tour.keys()} for
        tour in tours]
    tours_filtered = [tour for tour in tours_filtered if
                      not (tour['type'] != 'tour_recorded' or tour[
                          'sport'] != 'touringbicycle')]
    return tours_filtered