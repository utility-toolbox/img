# -*- coding=utf-8 -*-
r"""

"""
import typing as t
import requests
import rich
from rich.markup import escape
from ..constants import FileConflictStrategy
from ..core import downloader


__all__ = ['__cmd__']


def __cmd__(urls: t.Iterable[str], concurrent: int, on_conflict: FileConflictStrategy) -> None:
    console = rich.get_console()
    console._highlight = False

    def gen():
        nonlocal urls

        for url in urls:
            response = requests.get(url=url, stream=True, timeout=(10, 30))
            if not response.ok:
                console.print(f"[red]{response.status_code} {escape(url)}[/]")
                continue
            console.print(f"[green]{response.status_code} {escape(url)}[/]")
            yield response

    downloader(gen(), concurrent=concurrent, on_conflict=on_conflict)
