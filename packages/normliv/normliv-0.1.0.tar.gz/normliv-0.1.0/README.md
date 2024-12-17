# NormLiv

*NormLiv* is a Python package which quickly normalizes Livonian orthographies based on the chosen standard. It focuses on Unicode normalization to avoid confusions between diacritics and codes.

## Properties

Settings below are the default. They can be manually disabled:

- Removes the broken tone
- Replaces the vowels ǭ, y, ȳ, ü, ǖ
- Palatalized letters are normalized as described below
- Uses a *Normalization Form Canonical Composition* (NFC) Unicode transcription, where all combinable codepoints are composed.

> **Warning !** Because of the NFC conversion, some other characters might be affected. See more details [here](https://en.wikipedia.org/wiki/Unicode_equivalence#Normal_forms)


## Palatals

Latvian and Livonian palatalized consonants are written with a comma below or above. However, when Latvian (and Livonian) needed to be represented as codepoints in the 90s, the first unicode standard used characters labelled "with cedilla", although they are represented with a comma. Nowadays, the cedilla is still used but displayed as a comma for most consonants *except* t. The solution adopted here is the following:

- Replace cedilla by comma for t
- Replace comma by cedilla for other consonants.

The use of the comma (the only correct representation) can be enforced. See more on this issue:

- https://www.unicode.org/L2/L2013/13155r-cedilla-comma.pdf
- https://en.wikipedia.org/wiki/Cedilla
- http://diacritics.typo.cz/index.php?id=9

# Technical stuff

## Install

*NormLiv* is available through the PyPi repositories and can be installed via:

```
pip install normliv
```

## Usage

``` python
from normliv import normalize
text = '...'
print(normalize(text))
```

## Custom parameters

Parameters for the `normalize` function:

- text (str): The string to transliterate.
- tone (bool): Whether the tone should be kept. Defaults to False.
- eastern (bool): Whether the distinction between *ǭ* and *ō* should be kept. Defaults to False
- rounded (bool): Whether the *y/ü* and *ö* should be kept. Defaults to False.
- convention (str): Unicode convention to use. One of:
    - NFC (Composed, default)
    - NFD (Decomposed).

# TODO

- Handle caps
- More options for custom transcriptions
- More tests
