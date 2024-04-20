# -*- coding=utf-8 -*-
r"""

"""
from ._typing import *


__all__ = ['parse_timeout', 'parse_header', 'parse_referer']


def parse_timeout(timeout: str) -> T_TIMEOUT:
    a, sep, b = timeout.partition(':')
    if not sep:
        return float(a)
    return float(a) if a else None, float(b) if b else None


def parse_header(header: str) -> T_HEADER_PAIR:
    key, sep, value = header.partition(':')
    if not sep:
        raise ValueError(f"Invalid header format (expected 'key:value' got {header!r})")
    return key, value.lstrip(" ")


def parse_referer(referer: str) -> T_HEADER_PAIR:
    return "referer", referer
