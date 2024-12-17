import pytest
from normliv import normalize
import unicodedata


def test_normalize():
    chars = "āǭǬȯȮȱȰțȚḑḐņŅļĻŗ"
    chars_w = "āōŌȯȮȱȰțȚḑḐņŅļĻŗ"
    for char in chars:
        assert normalize(char, eastern=True) == char
        assert normalize(char, eastern=True, convention='NFD') == unicodedata.normalize('NFD', char)
    assert normalize(chars, eastern=False) == chars_w
