# -*- coding=utf-8 -*-
r"""

"""
import re
import enum
import typing as t
import operator


__all__ = ['FileConflictStrategy', 'SizeComparison']


class FileConflictStrategy(enum.Enum):
    rename = enum.auto()  # rename downloaded file 'file (1).ext'
    skip = enum.auto()  # skips current download
    replace = enum.auto()  # replace existing file

    def __str__(self):
        return self.name

    @classmethod
    def from_string(cls, string: str) -> 'FileConflictStrategy':
        try:
            return cls[string]
        except KeyError:
            raise ValueError(f'Unknown conflict strategy {string!r}'
                             f' ({", ".join(FileConflictStrategy.__members__)})') from None


_OP_MAP = {
    '!': operator.ne,
    '<=': operator.le,
    '<': operator.lt,
    '=': operator.eq,
    '>=': operator.ge,
    '>': operator.gt,
}


class SizeComparison:
    op: t.Callable[[int, int], bool]
    value: int

    def __init__(self, value: str):
        opkeys = '|'.join(re.escape(key) for key in _OP_MAP.keys())
        match = re.search(fr'^(?P<op>{opkeys})?(?P<num>\d+)$', value)
        if match is None:
            raise ValueError(f"Can't parse {value!r}. (allowed operators {', '.join(_OP_MAP.keys())})")
        self.op = _OP_MAP.get(match.group('op'), operator.eq)
        self.value = int(match.group('num'))

    def __call__(self, other: int) -> bool:
        return self.op(self.value, other)
