import random
import re


def random_color() -> str:
    """
    This method is creating a Hex color code randomly.

    Returns:
        str: Hex color code with a ``#`` at the beginning.
    """
    return "#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])


def remove_special_characters(string: str) -> str:
    """
    This method is replacing ``ä``, ``ö`` and ``ü`` by ``ae``, ``oe`` and
    ``ue`` and replaces the remaining special characters by ``_``.
    Args:
        string (str): input string

    Returns:
        str: modified input string, that does not contain special characters
    """
    string = string.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").\
        replace("ß", "ss")
    return re.sub('[^A-Za-z0-9]+', '_', string)
