# -*- coding=utf-8 -*-
r"""

"""
import signal
import threading
import typing as t


__all__ = ['CatchSignInt']


class CatchSignInt:
    _event: t.Optional['threading.Event'] = None

    def __enter__(self) -> 'threading.Event':
        self._event = threading.Event()
        self._override_handler()
        return self._event

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._restore_handler()
        self._event = None

    def _override_handler(self):
        signal.signal(signal.SIGINT, self._handler)

    def _handler(self, _signum, _frame):
        self._event.set()

    @staticmethod
    def _restore_handler():
        signal.signal(signal.SIGINT, signal.default_int_handler)
