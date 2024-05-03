# -*- coding=utf-8 -*-
r"""

"""
import typing as t
from .._typing import *
from ..constants import FileConflictStrategy


__all__ = ['__cmd__']


def __cmd__(urls: str, max_skip: int,
            concurrent: int, on_conflict: 'FileConflictStrategy', headers: T_HEADERS, timeout: T_TIMEOUT) -> None:
    import rich
    from rich.markup import escape
    import requests
    from ..core import downloader

    console = rich.get_console()
    console._highlight = False

    def gen():
        nonlocal urls

        for raw_url in urls:
            fail_count = 0

            for url in iter_urls(base=raw_url):
                response = requests.get(url=url, stream=True, headers=dict(headers), timeout=timeout)
                if not response.ok:
                    console.print(f"[red]{response.status_code} {escape(url)}[/]", highlight=False)
                    fail_count += 1
                    if fail_count <= max_skip:
                        continue  # next
                    else:
                        break  # stop
                console.print(f"[green]{response.status_code} {escape(url)}[/]", highlight=False)
                yield response, None

    downloader(gen(), concurrent=concurrent, on_conflict=on_conflict)


def iter_urls(base: str) -> t.Iterator[str]:
    r"""
    infinitely generate next url based on incrementing {0} parts in the url
    """
    import re

    url_template = prepare_url(url=base)

    def repl(match: re.Match) -> str:
        num_str = match.group(1)
        return str(int(num_str) + i).rjust(len(num_str), "0")

    i = 0

    while True:
        yield re.sub(r"\{(\d+)}", repl, url_template)
        i += 1


def prepare_url(url: str) -> str:
    r"""
    adds {0} around the last number in the url-path if not already present anywhere.
    """
    import re
    import urllib.parse as urlparse

    # already prepared
    if re.search(r"\{\d+}", url) is not None:
        return url

    parsed = urlparse.urlparse(url)
    matches = list(re.finditer(r"\d+", parsed.path))
    if not matches:
        raise ValueError(f"Failed to identify increment in provided url ({url!r}")
    match = matches[-1]
    start, num_str, stop = match.start(), match.group(), match.end()
    return parsed._replace(path=f"{parsed.path[:start]}{{{num_str}}}{parsed.path[stop:]}").geturl()
