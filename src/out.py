import os

from helpers import random_color


def write_gpx(path: str, gpx_txt: str) -> None:
    """
    This method writes the gpx file.
    Args:
        path (str): file path of the output file
        gpx_txt (str): content, that shall be written to the output file

    Returns:
        None
    """
    f = open(path, 'w', encoding="utf-8")
    f.write(gpx_txt)
    f.close()
    return None


def meta_script(dict_of_trips: dict, output_folder: str) -> None:
    """
    This method is creating the file meta.js, to be used by the frontend with
    the following code: https://github.com/fraden/routes
    Args:
        dict_of_trips (dict): containing trip meta information
        output_folder (str): defines the output folder for the gpx files

    Returns:
        None
    """
    text = "const colors = require('tailwindcss/colors') " \
           "// eslint-disable-line \nconst meta ={\n"
    for key in dict_of_trips:
        text = text + key + ": {\ndescription:\n'" + dict_of_trips[key][
            'description'] + "',\nrating:5,\nlocation: 'Germany', color:'" \
               + random_color() + "',\nadded:'2020-01-01'},"

    text = text + "}\nmodule.exports = { meta }"
    f = open(os.path.join(output_folder, "meta.js"), 'w', encoding="utf-8")
    f.write(text)
    f.close()
    return None
