# -*- coding=utf-8 -*-
r"""

"""
import signal
import threading
import typing as t
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import requests
import rich.progress
from ..util import get_progress_columns, extract_content_size, extract_filename, get_free_filename


def __cmd__(urls: t.Iterable[str], concurrent: int, overwrite: bool) -> None:
    urls = list(urls)
    canceled = threading.Event()

    def handle_sigint(_sig, _frame) -> None:
        nonlocal canceled, progress, default_sigint
        canceled.set()
        progress.console.print("graceful shutdown initiated")
        signal.signal(signal.SIGINT, default_sigint)

    default_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, handle_sigint)

    with (
        rich.progress.Progress(*get_progress_columns(),
                               auto_refresh=True, refresh_per_second=5, expand=True) as progress,
        ThreadPoolExecutor(max_workers=concurrent) as pool,
    ):
        for url in urls:
            if canceled.is_set():
                break
            response = requests.get(url, stream=True, timeout=(10, 30))
            if not response.ok:
                progress.console.print(f"[red]{response.status_code} {url}[/]")
                continue
            progress.console.print(f"[green]{response.status_code} {url}[/]")
            pool.submit(handle_response, response=response, progress=progress, canceled=canceled, overwrite=overwrite)
        progress.console.print(
            rich.progress.Spinner("dots", text="Waiting for downloads to finnish...")
        )
    progress.refresh()  # on last time


# todo: catch errors
def handle_response(response: requests.Response, progress: rich.progress.Progress, canceled: threading.Event,
                    overwrite: bool) -> None:
    filename = extract_filename(response)
    if not overwrite:
        filename = get_free_filename(filename)
    filepath = Path(filename)
    filepath.touch(exist_ok=False)  # ensure it exist for other threads/downloads
    tmpfile = filepath.with_stem(f".{filepath.stem}")
    task_id = progress.add_task(description=filepath.name, start=True, total=extract_content_size(response))

    with open(tmpfile, 'wb') as file:
        for chunk in response.iter_content(chunk_size=1024*10):
            if canceled.is_set():
                tmpfile.unlink(missing_ok=True)  # is this a problem with file.close()?
                return
            progress.update(task_id, advance=len(chunk))
            file.write(chunk)

    filepath.unlink(missing_ok=True)  # remove old
    tmpfile.rename(filepath)  # tmpfile -> file
    progress.remove_task(task_id)  # remove now unnecessary progress bar
    progress.console.print(f"{filepath} is done")  # but keep a log
