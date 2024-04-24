# -*- coding=utf-8 -*-
r"""

"""
import re
import os
import os.path as p
import typing as t
if t.TYPE_CHECKING:
    from requests import Response


__all__ = ['extract_content_size', 'extract_filename', 'get_free_filename', 'is_image_response']


def extract_content_size(response: 'Response') -> t.Optional[int]:
    r"""
    attempts to extract the content size of a given response
    """
    try:
        content_size = response.headers['Content-Length']
    except KeyError:
        content_size = None
    else:
        content_size = int(content_size)
    return content_size


def extract_filename(response: 'Response') -> str:
    r"""
    extracts the filename from the 'Content-Disposition' header with fallback to the url-path or finally the hostname
    """
    import urllib.parse as urlparse

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


def get_free_filename(fn: t.Union[str, os.PathLike]) -> str:
    r"""
    find a free filename given a filename path
    """
    i = 0
    dirname, filename = p.split(fn)
    name, ext = p.splitext(filename)
    while p.isfile(p.join(dirname, filename)) or p.isfile(p.join(dirname, f".{filename}")):
        i += 1
        filename = f"{name} ({i}){ext}"
    return p.join(dirname, filename)


def is_image_response(response: 'Response') -> bool:
    r"""
    checks if the content type is 'image/*'
    """
    try:
        content_type: str = response.headers["Content-Type"]
    except KeyError:
        return False
    else:
        return content_type.startswith("image/")
