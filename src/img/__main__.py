# -*- coding=utf-8 -*-
r"""

"""
import argparse as ap
from . import __version__, __cmd__, constants
try:
    import runpy
    import rich.traceback
    rich.traceback.install(show_locals=True, suppress=[runpy])
except ModuleNotFoundError:
    pass


parser = ap.ArgumentParser(prog="img", formatter_class=ap.ArgumentDefaultsHelpFormatter)
parser.set_defaults(cmd=parser.print_help)
parser.add_argument('-v', '--version', action='version', version=__version__)
subparsers = parser.add_subparsers()

get_parser = subparsers.add_parser("get", formatter_class=ap.ArgumentDefaultsHelpFormatter)
get_parser.set_defaults(cmd=__cmd__.wget.__cmd__)
get_parser.add_argument('-c', '--concurrent', type=int, default=3,
                        help="Number of concurrent downloads")
get_parser.add_argument('--on-conflict', type=constants.FileConflictStrategy.from_string,
                        default=constants.FileConflictStrategy.rename, choices=list(constants.FileConflictStrategy),
                        help="How to handle conflict of filenames during download")
get_parser.add_argument("urls", nargs=ap.ONE_OR_MORE,
                        help="URLs to download")


def main():
    args = vars(parser.parse_args())
    cmd = args.pop('cmd')
    return cmd(**args)


if __name__ == '__main__':
    main()
