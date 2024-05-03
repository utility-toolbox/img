# -*- coding=utf-8 -*-
r"""

"""
import typing as t
from .._typing import *
from ..constants import *


__all__ = ['__cmd__']


def __cmd__(site: T_URL, linked: bool, width: t.Optional[SizeComparison], height: t.Optional[SizeComparison],
            concurrent: int, on_conflict: FileConflictStrategy, headers: T_HEADERS, timeout: T_TIMEOUT) -> None:
    import urllib.parse as urlparse
    import bs4
    import requests
    import rich
    from rich.markup import escape
    from ..core import downloader
    from ..util import is_image_response, get_image_size, UnknownImageFormatError

    console = rich.get_console()
    console._highlight = False

    def gen():
        nonlocal site

        response = requests.get(site, headers=dict(headers), timeout=timeout)
        response.raise_for_status()
        content_type = response.headers.get('Content-Type', "")
        if content_type != "text/html":
            print(f"[yellow]Bad Content-Type ({content_type!r})")

        html: str = response.content

        soup = bs4.BeautifulSoup(html, 'html.parser')
        urls: t.List[str] = []
        if linked:
            for link in soup.select('a[href]:has(img[src])'):
                url = urlparse.urljoin(site, link['href'])
                if url not in urls:
                    urls.append(url)
        for img in soup.select('img[src]'):
            url = urlparse.urljoin(site, img['src'])
            if url not in urls:
                urls.append(url)

        urls = [url for url in urls if url.startswith("http")]

        for url in urls:
            response = requests.get(url=url, stream=True, headers=dict(headers), timeout=timeout)
            if not response.ok:
                console.print(f"[red]{response.status_code} {escape(url)}[/]")
                continue
            if not is_image_response(response):
                console.print(f"[red]Not an Image: {escape(url)}[/]")
                continue
            head = None
            if width or height:
                head = response.raw.read(1024)
                try:
                    resp_width, resp_height = get_image_size(head)
                except UnknownImageFormatError as err:
                    console.print(f"[red]{type(err).__name__}: {err!s} ({escape(url)})[/]")
                    continue
                if width and not width(resp_width):
                    console.print(f"[red]Bad Width: {escape(url)}[/]")
                    continue
                if height and not height(resp_height):
                    console.print(f"[red]Bad Height: {escape(url)}[/]")
                    continue
            console.print(f"[green]{response.status_code} {escape(url)}[/]")
            yield response, head

    downloader(gen(), concurrent=concurrent, on_conflict=on_conflict)
