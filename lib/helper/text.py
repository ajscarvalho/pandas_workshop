# -*- coding: utf-8 -*-


from unidecode import unidecode
import re

_non_word_matcher = re.compile("[^\w]+")


def canonicalize(text):
    normalized = unidecode(text)
    return _non_word_matcher.sub('_', normalized).lower()


def is_numeric(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
