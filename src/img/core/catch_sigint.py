# -*- coding=utf-8 -*-
r"""

"""
import signal
import threading
import typing as t


__all__ = ['CatchSigInt']


class CatchSigInt:
    _old_handler: t.Optional[t.Callable] = None
    _event: t.Optional['threading.Event'] = None

    def __enter__(self) -> 'threading.Event':
        self._event = threading.Event()
        self._override_handler()
        return self._event

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._restore_handler()
        self._event = None

    def _override_handler(self):
        self._old_handler = signal.getsignal(signal.SIGINT)
        signal.signal(signal.SIGINT, self._handler)

    def _handler(self, _signum, _frame):
        self._event.set()

    def _restore_handler(self):
        signal.signal(signal.SIGINT, self._old_handler)
