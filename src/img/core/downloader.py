# -*- coding=utf-8 -*-
r"""

"""
import threading
import typing as t
from concurrent.futures import ThreadPoolExecutor, Future

import requests
import rich.progress
import rich.traceback

from ..util import get_progress_columns
from .catch_sigint import CatchSignInt
from .handle_download import handle_download


__all__ = ['downloader']


def downloader(gen: t.Iterator[requests.Response], concurrent: int = 4, overwrite: bool = False):
    with (
        CatchSignInt() as canceled,
        rich.progress.Progress(*get_progress_columns(),
                               auto_refresh=True, refresh_per_second=5, expand=True) as progress,
        ThreadPoolExecutor(max_workers=concurrent) as pool,
    ):
        counter = threading.Semaphore(concurrent)
        for response in gen:
            counter.acquire()
            fut: Future = pool.submit(handle_download,
                                      response=response, progress=progress, canceled=canceled, overwrite=overwrite)

            @fut.add_done_callback
            def done(future: Future) -> None:
                counter.release()
                error = future.exception()
                if error:
                    progress.console.print(
                        rich.traceback.Traceback.from_exception(
                            type(error), error, error.__traceback__,
                        )
                    )
