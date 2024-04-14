# -*- coding=utf-8 -*-
r"""

"""
import enum


__all__ = ['FileConflictStrategy']


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
            raise ValueError(f'Unknown conflict strategy {string!r} ({", ".join(FileConflictStrategy.__members__)})') from None
