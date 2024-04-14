# -*- coding=utf-8 -*-
r"""

"""
import typing as t
import requests
import rich
from ..core import downloader


__all__ = ['__cmd__']


def __cmd__(urls: t.Iterable[str], concurrent: int, overwrite: bool) -> None:
    console = rich.get_console()

    def gen():
        nonlocal urls

        for url in urls:
            response = requests.get(url, stream=True, timeout=(10, 30))
            if not response.ok:
                console.print(f"[red]{response.status_code} {url}[/]")
                continue
            console.print(f"[green]{response.status_code} {url}[/]")
            yield response

    downloader(gen(), concurrent=concurrent, overwrite=overwrite)