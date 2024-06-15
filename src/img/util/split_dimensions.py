# -*- coding=utf-8 -*-
r"""

"""
import typing as t


__all__ = ['split_dimensions']


def split_dimensions(dimension: str) -> t.Tuple[int, int]:
    import re
    match = re.search(r'(\d+)x(\d+)', dimension)
    if match is None:
        raise ValueError(f'Invalid dimension: {dimension} (expected: 0x0)')
    return int(match.group(1)), int(match.group(2))
