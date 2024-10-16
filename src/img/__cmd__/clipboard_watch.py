# -*- coding=utf-8 -*-
r"""

"""
import typing as t
from .._typing import *
from ..constants import FileConflictStrategy


__all__ = ['__cmd__']


def __cmd__(pause: float, concurrent: int, on_conflict: FileConflictStrategy, headers: T_HEADERS, timeout: T_TIMEOUT):
    import requests
    import rich
    from rich.markup import escape
    from ..util import is_image_response
    from ..core import downloader

    console = rich.get_console()
    console._highlight = False

    def gen():
        for url in clipboard_watch(pause=pause):
            response = requests.get(url=url, stream=True, headers=dict(headers), timeout=timeout)
            if not response.ok:
                console.print(f"[red]{response.status_code} {escape(url)}[/]")
                continue
            if not is_image_response(response):
                console.print(f"[yellow]Not an Image: {escape(url)}[/]")
            console.print(f"[green]{response.status_code} {escape(url)}[/]")
            yield response, None

    downloader(gen(), concurrent=concurrent, on_conflict=on_conflict)


def clipboard_watch(pause: float = 0.1) -> t.Iterator[str]:
    import time
    import pyperclip
    recent_value = None
    while True:
        current_value = pyperclip.paste()
        if current_value != recent_value:
            recent_value = current_value
            if is_valid_url(current_value):
                yield current_value
        time.sleep(pause)


def is_valid_url(url: str) -> bool:
    from urllib.parse import urlparse
    parsed = urlparse(url)
    return bool(parsed.scheme) and bool(parsed.netloc)
