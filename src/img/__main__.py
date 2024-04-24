# -*- coding=utf-8 -*-
r"""
cli to automatically download a collection of images or scrape them from a website
"""
import argparse as ap
from . import __version__, __cmd__, constants
from . import _install_traceback  # noqa
from .__cli_util__ import *


def add_common_headers(p: ap.ArgumentParser) -> None:
    p.add_argument('-c', '--concurrent', type=int, default=3,
                   help="Number of concurrent downloads")
    p.add_argument('--on-conflict', type=constants.FileConflictStrategy.from_string,
                   default=constants.FileConflictStrategy.rename, choices=list(constants.FileConflictStrategy),
                   help="How to handle conflict of filenames during download")
    p.add_argument('--timeout', type=parse_timeout, default=(10, 30),
                   help="Specify timeout. Either 'x.y' for general timeout"
                        " or 'a.b:c.d' for connect:read timeouts")
    p.add_argument('--header', action='append', dest='headers', type=parse_header,
                   help="Add an additional header")
    p.add_argument('--referer', action='append', dest='headers', type=parse_referer,
                   help="Add the referer header")


parser = ap.ArgumentParser(prog="img", formatter_class=ap.ArgumentDefaultsHelpFormatter, description=__doc__)
parser.set_defaults(cmd=parser.print_help)
parser.add_argument('-v', '--version', action='version', version=__version__)
subparsers = parser.add_subparsers()

collect_parser = subparsers.add_parser("collect", formatter_class=ap.ArgumentDefaultsHelpFormatter,
                                       help="Collects images.",
                                       description="Manually add one or more {0} to specify which numbers"
                                                   " should increment for the next url")
collect_parser.set_defaults(cmd=__cmd__.collect.__cmd__)
add_common_headers(p=collect_parser)
collect_parser.add_argument('--max-skip', type=int, default=0,
                            help="How many url can be failing before stopping searching")
collect_parser.add_argument("urls", nargs=ap.ONE_OR_MORE,
                            help="URLs to collect from")

scrape_parser = subparsers.add_parser("scrape", formatter_class=ap.ArgumentDefaultsHelpFormatter,
                                      help="Scrapes images from given URL")
scrape_parser.set_defaults(cmd=__cmd__.scrape.__cmd__)
add_common_headers(p=scrape_parser)
scrape_parser.add_argument('--linked', action=ap.BooleanOptionalAction,
                           help="whether to attempt to download <a href=\"...\"><img/></a> urls")
scrape_parser.add_argument("site",
                           help="Site to scrape")

get_parser = subparsers.add_parser("get", formatter_class=ap.ArgumentDefaultsHelpFormatter,
                                   help="similar to the `wget` program. used to download provided images")
get_parser.set_defaults(cmd=__cmd__.wget.__cmd__)
add_common_headers(p=get_parser)
get_parser.add_argument("urls", nargs=ap.ONE_OR_MORE,
                        help="URLs to download")


def main():
    args = vars(parser.parse_args())
    cmd = args.pop('cmd')
    return cmd(**args)


if __name__ == '__main__':
    main()
