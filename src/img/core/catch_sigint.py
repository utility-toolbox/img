# -*- coding=utf-8 -*-
r"""

"""
import signal
import threading
import typing as t


__all__ = ['CatchSignInt']


class CatchSignInt:
    _event: t.Optional[threading.Event] = None

    def __enter__(self) -> threading.Event:
        self._event = threading.Event()
        signal.signal(signal.SIGINT, lambda _s, _f: self._event.set())
        return self._event

    def __exit__(self, exc_type, exc_val, exc_tb):
        signal.signal(signal.SIGINT, signal.default_int_handler)
        self._event = None
