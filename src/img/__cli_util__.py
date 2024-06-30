# -*- coding=utf-8 -*-
r"""

"""
from ._typing import *


__all__ = [
    'parse_timeout', 'parse_header', 'parse_referer',
    'parse_keyval',
    'split_dimensions',
]


def parse_timeout(timeout: str) -> T_TIMEOUT:
    r""" parses '[.0]' or '[.0]:[.0]' """
    a, sep, b = timeout.partition(':')
    if not sep:
        return float(a)
    return float(a) if a else None, float(b) if b else None


def parse_header(header: str) -> T_HEADER_PAIR:
    r""" parses 'key: value' """
    key, sep, value = header.partition(':')
    if not sep:
        raise ValueError(f"Invalid header format (expected 'key:value' got {header!r})")
    return key, value.lstrip(" ")


def parse_referer(referer: str) -> T_HEADER_PAIR:
    return "referer", referer


def parse_keyval(keyval: str):
    r""" parses 'key=value' """
    from ast import literal_eval
    key, sep, val = keyval.partition('=')
    if not sep:
        raise ValueError(f"Invalid key-value format (expected 'key=value' got {keyval!r})")
    try:
        val = literal_eval(val)
    except (ValueError, SyntaxError):
        pass
    return key, val


def split_dimensions(dimension: str) -> T_DIMENSIONS:
    r""" parses '[0]x[0]' """
    import re
    match = re.search(r'(-?\d+)x(-?\d+)', dimension)
    if match is None:
        raise ValueError(f'Invalid dimension: {dimension} (expected format: [0]x[0])')
    return int(match.group(1)), int(match.group(2))
