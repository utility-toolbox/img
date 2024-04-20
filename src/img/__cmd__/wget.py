# -*- coding=utf-8 -*-
r"""

"""
import requests
import rich
from rich.markup import escape
from .._typing import *
from ..constants import FileConflictStrategy
from ..core import downloader


__all__ = ['__cmd__']


def __cmd__(urls: T_URLS,
            concurrent: int, on_conflict: FileConflictStrategy, headers: T_HEADERS, timeout: T_TIMEOUT) -> None:
    console = rich.get_console()
    console._highlight = False

    def gen():
        nonlocal urls

        for url in urls:
            response = requests.get(url=url, stream=True, headers=dict(headers), timeout=timeout)
            if not response.ok:
                console.print(f"[red]{response.status_code} {escape(url)}[/]")
                continue
            console.print(f"[green]{response.status_code} {escape(url)}[/]")
            yield response

    downloader(gen(), concurrent=concurrent, on_conflict=on_conflict)
