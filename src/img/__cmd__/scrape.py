# -*- coding=utf-8 -*-
r"""

"""
import typing as t
import urllib.parse as urlparse
import bs4
import requests
import rich
from rich.markup import escape
from .._typing import *
from ..constants import FileConflictStrategy
from ..core import downloader
from ..util import is_image_response


__all__ = ['__cmd__']


def __cmd__(site: T_URL, linked: bool,
            concurrent: int, on_conflict: FileConflictStrategy, headers: T_HEADERS, timeout: T_TIMEOUT) -> None:
    console = rich.get_console()
    console._highlight = False

    def gen():
        nonlocal site

        response = requests.get(site, headers=dict(headers), timeout=timeout)
        response.raise_for_status()
        content_type = response.headers.get('Content-Type', "")
        if not content_type != "text/html":
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
                console.print(f"[red]Not-Image: {escape(url)}[/]")
                continue
            console.print(f"[green]{response.status_code} {escape(url)}[/]")
            yield response

    downloader(gen(), concurrent=concurrent, on_conflict=on_conflict)
