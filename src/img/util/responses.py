# -*- coding=utf-8 -*-
r"""

"""
import re
import typing as t
import os.path as p
import urllib.parse as urlparse
from requests import Response


__all__ = ['extract_content_size', 'extract_filename', 'get_free_filename', 'is_image_response']


def extract_content_size(response: Response) -> t.Optional[int]:
    try:
        content_size = response.headers['Content-Length']
    except KeyError:
        content_size = None
    else:
        content_size = int(content_size)
    return content_size


def extract_filename(response: Response) -> str:
    content_disposition = response.headers.get('Content-Disposition')
    if content_disposition:
        match = next(re.finditer(r'filename=(.+)', content_disposition), None)
        if match:
            return urlparse.unquote(match.lastgroup)

    url = urlparse.urlparse(response.url)
    parts = list(filter(None, url.path.rsplit('/')))
    if parts:
        return urlparse.unquote(parts[-1])

    return urlparse.unquote(url.hostname)


def get_free_filename(fn: str) -> str:
    i = 0
    name, ext = p.splitext(fn)
    while p.isfile(fn):
        i += 1
        fn = f"{name} ({i}){ext}"
    return fn


def is_image_response(response: Response) -> bool:
    try:
        content_type: str = response.headers["Content-Type"]
    except KeyError:
        return False
    else:
        return content_type.startswith("image/")
