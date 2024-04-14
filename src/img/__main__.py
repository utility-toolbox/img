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

collect_parser = subparsers.add_parser("collect", formatter_class=ap.ArgumentDefaultsHelpFormatter,
                                       help="Collects images. Manually add 1+ {0} to specify which numbers should"
                                            " increment for the next url")
collect_parser.set_defaults(cmd=__cmd__.collect.__cmd__)
collect_parser.add_argument('-c', '--concurrent', type=int, default=3,
                            help="Number of concurrent downloads")
collect_parser.add_argument('--on-conflict', type=constants.FileConflictStrategy.from_string,
                            default=constants.FileConflictStrategy.rename, choices=list(constants.FileConflictStrategy),
                            help="How to handle conflict of filenames during download")
collect_parser.add_argument('--max-skip', type=int, default=0,
                            help="How many url can be failing before stopping searching")
collect_parser.add_argument("urls", nargs=ap.ONE_OR_MORE,
                            help="URLs to collect from")

get_parser = subparsers.add_parser("get", formatter_class=ap.ArgumentDefaultsHelpFormatter,
                                   help="similar to the `wget` program. used to download provided images")
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
