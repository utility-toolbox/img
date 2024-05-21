# -*- coding=utf-8 -*-
r"""

"""
import threading
import typing as t
from .._typing import *
from ..util import get_progress_columns
from ..constants import FileConflictStrategy
from .catch_sigint import CatchSigInt
from .handle_download import handle_download


__all__ = ['downloader']


def downloader(gen: t.Iterator[T_GENITEM], concurrent: int = 4,
               on_conflict: 'FileConflictStrategy' = FileConflictStrategy.rename):
    import rich.progress
    import rich.traceback
    from concurrent.futures import ThreadPoolExecutor, Future

    with (
        CatchSigInt() as canceled,
        rich.progress.Progress(*get_progress_columns(),
                               auto_refresh=True, refresh_per_second=5, expand=True) as progress,
        ThreadPoolExecutor(max_workers=concurrent) as pool,
    ):
        counter = threading.Semaphore(concurrent)
        for response, head in gen:
            while not counter.acquire(timeout=0.1) and not canceled.is_set():
                pass
            if canceled.is_set():
                break

            job: Future = pool.submit(handle_download,
                                      response=response, head=head, progress=progress,
                                      canceled=canceled, on_conflict=on_conflict)

            @job.add_done_callback
            def done(future: Future) -> None:
                counter.release()
                error = future.exception()
                if error:
                    progress.console.print(
                        rich.traceback.Traceback.from_exception(
                            type(error), error, error.__traceback__,
                        )
                    )
