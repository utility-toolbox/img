# -*- coding=utf-8 -*-
r"""

"""
import argparse as ap
from ._typing import *


__all__ = ['parse_timeout', 'parse_header', 'parse_referer', 'AutocompleteAction']


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


class AutocompleteAction(ap.Action):
    def __init__(self, option_strings, dest, help=None):
        super().__init__(
            option_strings=option_strings,
            dest=ap.SUPPRESS,
            nargs=ap.OPTIONAL,
            const="bash",
            # default="bash",
            choices=("bash", "zsh", "tcsh", "fish", "powershell"),
            help=help,
        )

    def __call__(self, parser: ap.ArgumentParser, _namespace, values, _option_string=None):
        import os
        import sys
        import argcomplete
        sys.stdout.write(argcomplete.shellcode(
            executables=['./img'] if os.getenv("_IMG_DEBUG_LOCAL") is not None else ['img'],
            use_defaults=False,
            shell=values,
        ))
        parser.exit(0)
