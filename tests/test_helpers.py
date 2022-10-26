import string

from src import helpers


def test_random_color_starts_with_hash():
    color = helpers.random_color()
    assert color[0] == '#'


def test_random_color_has_only_hex_numbers():
    color = helpers.random_color()
    assert all(c in string.hexdigits for c in color[1:])


def test_random_color_has_correct_length():
    color = helpers.random_color()
    assert len(color) == 7


def test_remove_special_characters_for_ae():
    string_1 = "Bär"
    assert helpers.remove_special_characters(string_1) == "Baer"


def test_remove_special_characters_for_ue():
    string_1 = "Tür"
    assert helpers.remove_special_characters(string_1) == "Tuer"


def test_remove_special_characters_for_oe():
    string_1 = "Löwe"
    assert helpers.remove_special_characters(string_1) == "Loewe"


def test_remove_special_characters_for_ss():
    string_1 = "Spaß"
    assert helpers.remove_special_characters(string_1) == "Spass"


def test_remove_special_characters_for_special_character():
    string_1 = "Haee.#+?=dkkd"
    assert helpers.remove_special_characters(string_1) == "Haee_dkkd"


def test_remove_special_characters_for_ae_and_special_character():
    string_1 = "Hä.i?"
    assert helpers.remove_special_characters(string_1) == "Hae_i_"
