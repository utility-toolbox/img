# -*- coding=utf-8 -*-
r"""

"""
import argparse as ap
from . import __version__, get as img_get
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

get_parser = subparsers.add_parser("get")
get_parser.set_defaults(cmd=img_get.__cmd__)
get_parser.add_argument('-c', '--concurrent', type=int, default=3,
                        help="Number of concurrent downloads")
get_parser.add_argument('--overwrite', action=ap.BooleanOptionalAction, default=False,
                        help="overwrite existing files or create 'file (1).ext'")
get_parser.add_argument("urls", nargs=ap.ONE_OR_MORE,
                        help="URLs to download")


def main():
    args = vars(parser.parse_args())
    cmd = args.pop('cmd')
    return cmd(**args)


if __name__ == '__main__':
    main()
