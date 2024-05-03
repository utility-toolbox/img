# -*- coding=utf-8 -*-
r"""

"""
import typing as t
if t.TYPE_CHECKING:
    import requests


__all__ = [
    'T_URL', 'T_URLS', 'T_TIMEOUT', 'T_CONCURRENT', 'T_HEADER_PAIR', 'T_HEADERS',
    'T_GENITEM',
]


T_URL: t.TypeAlias = str
T_URLS: t.TypeAlias = t.List[T_URL]
T_TIMEOUT: t.TypeAlias = t.Union[float, t.Tuple[float, float]]
T_CONCURRENT: t.TypeAlias = int
T_HEADER_PAIR: t.TypeAlias = t.Tuple[str, str]
T_HEADERS: t.TypeAlias = t.List[T_HEADER_PAIR]

T_GENITEM: t.TypeAlias = t.Tuple['requests.Response', t.Optional[bytes]]
