# -*- coding=utf-8 -*-
r"""
cli to automatically download a collection of images or scrape them from a website
"""
import argparse as ap
from shell_complete import ShellCompleteAction, Recommended as ShellRecommended, types
from . import __version__, __cmd__, constants
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
    p.add_argument('--header', action='append', dest='headers', default=[], type=parse_header,
                   help="Add an additional header")
    p.add_argument('--referer', action='append', dest='headers', type=parse_referer,
                   help="Add the referer header")


parser = ap.ArgumentParser(prog="img", formatter_class=ap.ArgumentDefaultsHelpFormatter, description=__doc__)
parser.set_defaults(cmd=parser.print_help)
parser.add_argument('-v', '--version', action='version', version=__version__)
parser.add_argument('--shell-completion', action=ShellCompleteAction,
                    help="Generates an auto-complete shell script. Use with `eval \"$(img --shell-completion)\"`")
subparsers = parser.add_subparsers()

#

collect_parser = subparsers.add_parser("collect", formatter_class=ap.ArgumentDefaultsHelpFormatter,
                                       help="Collects images",
                                       description="Manually add one or more {0} to specify which numbers"
                                                   " should increment for the next url")
collect_parser.set_defaults(cmd=__cmd__.collect.__cmd__)
add_common_headers(p=collect_parser)
collect_parser.add_argument('--max-skip', type=int, default=0,
                            help="How many url can be failing before stopping searching")
collect_parser.add_argument("urls", nargs=ap.ONE_OR_MORE,
                            help="URLs to collect from")

#

merge_parser = subparsers.add_parser("merge", formatter_class=ap.ArgumentDefaultsHelpFormatter,
                                     help="Merges multiple images into one image",
                                     epilog="img merge output.png --save method=6 2x1 left.png right.png")
merge_parser.set_defaults(cmd=__cmd__.merge.__cmd__)
merge_parser.add_argument('-y', '--yes', action='store_true', default=False,
                          help="Overwrite output if it exists")
merge_parser.add_argument('--save', action='append', type=parse_keyval, dest='save_args', default=[],
                          help="Additional arguments to the PIL.Image.Image.save() method in format of 'key=value'."
                               " (https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html)")
merge_parser.add_argument('--mode', default='RGB',
                          help="In case you need to convert an image with alpha layer (e.g. png)"
                               " to one without (e.g. jpeg)."
                               " (https://pillow.readthedocs.io/en/stable/handbook/concepts.html#modes)") \
    .completer = ShellRecommended("RGB", "RGBA", "1", "L", "CMYK", "LAB", "HSV")
merge_parser.add_argument('output', type=types.file,
                          help="Output file to write to")
merge_parser.add_argument('dimensions', type=split_dimensions,
                          help="Dimensions of the output image (not in pixels) (eg 2x2)")
merge_parser.add_argument('images', type=types.file, nargs=ap.ONE_OR_MORE,
                          help="Input Images to merge")

#

repack = subparsers.add_parser("repack", formatter_class=ap.ArgumentDefaultsHelpFormatter,
                               help="Repacks an image to a different format or size",
                               epilog="img repack input.jpg output.png --size -1:480 --mode RGB --save method=6")
repack.set_defaults(cmd=__cmd__.repack.__cmd__)
repack.add_argument('-y', '--yes', action='store_true', default=False,
                    help="Overwrite output if it exists")
repack.add_argument('--save', action='append', type=parse_keyval, dest='save_args', default=[],
                    help="Additional arguments to the PIL.Image.Image.save() method in format of 'key=value'."
                         " (https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html)")
repack.add_argument('--mode',
                    help="In case you need to convert an image with alpha layer (e.g. png) to one without (e.g. jpeg)."
                         " (https://pillow.readthedocs.io/en/stable/handbook/concepts.html#modes)") \
    .completer = ShellRecommended("RGB", "RGBA", "1", "L", "CMYK", "LAB", "HSV")
repack_size_group = repack.add_mutually_exclusive_group()
repack_size_group.add_argument('--size', type=split_dimensions,
                               help="Specify the new image size. use -1 for width or height to keep the aspect")
repack_size_group.add_argument('--thumbnail', type=split_dimensions,
                               help="Keep aspect while resizing and don't grow in size (only scale down)")
repack.add_argument('source', type=types.file,
                    help="Source image to resize")
repack.add_argument('output', type=types.file,
                    help="Output file to write to")

#

scrape_parser = subparsers.add_parser("scrape", formatter_class=ap.ArgumentDefaultsHelpFormatter,
                                      help="Scrapes images from given URL")
scrape_parser.set_defaults(cmd=__cmd__.scrape.__cmd__)
add_common_headers(p=scrape_parser)
scrape_parser.add_argument('-l', '--linked', action=ap.BooleanOptionalAction,
                           help="whether to attempt to download <a href=\"...\"><img/></a> urls")
scrape_parser.add_argument('-W', '--width',
                           type=constants.SizeComparison, nargs=ap.OPTIONAL, const=">1000",
                           help="specify width (eg '>500')")
scrape_parser.add_argument('-H', '--height',
                           type=constants.SizeComparison, nargs=ap.OPTIONAL, const=">1000",
                           help="specify height (eg '>500')")
scrape_parser.add_argument("site",
                           help="Site to scrape")

#

get_parser = subparsers.add_parser("get", formatter_class=ap.ArgumentDefaultsHelpFormatter,
                                   help="Similar to the `wget` program. Used to download provided images")
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
