# NormLiv - Normalisation of Livonian Orthography
# Copyright (C) 2024  Jules Bouton
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import re
import unicodedata


def _replace(text, table):
    """ Replaces lower and upper chars for a conversion table"""
    for old, new in table.items():
        text = re.sub(old, new, text)
        text = re.sub(old.upper(), new.upper(), text)
    return text


def normalize(text, tone=False, eastern=False, rounded=False, convention='NFC'):
    """Normalizes a text in Livonian orthography,

    Arguments:
        text (str): The string to transliterate
        tone (bool): Whether the tone should be kept.
            Defaults to False.
        eastern (bool): Whether the distinction between ǭ and ō
            should be kept. Defaults to False.
        rounded (bool): Whether the y/ü and ö should be kept.
            Defaults to False.
        convention (str): Unicode convention to use. One of:
            NFC (Composed, default), NFD (Decomposed).
    """

    # Temporary switch to composed characters for uniformity.
    text = unicodedata.normalize('NFC', text)

    # Transcribe cedillas / commas.
    palatals = {
        "ţ": "ț",  # T cedilla -> comma
        "d̦": "ḑ",  # D comma -> cedilla
        "n̦": "ņ",  # N comma -> cedilla
        "l̦": "ļ",  # L comma -> cedilla
        "r̦": "ŗ",  # R comma -> cedilla
        }
    text = _replace(text, palatals)

    # Optional changes
    if not tone:
        text = re.sub(r'[’]', '', text)
    if not eastern:
        long_o = {"ǭ": "ō"}
        text = _replace(text, long_o)
    if not rounded:
        round = {"y|ü": "i",
                 "ö": "e"}
        text = _replace(text, round)
    else:
        text = _replace(text, {"ü": "y"})

    # Transcribe to expected convention.
    text = unicodedata.normalize(convention, text)

    return text
