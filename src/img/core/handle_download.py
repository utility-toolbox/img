# -*- coding=utf-8 -*-
r"""

"""
import threading
from pathlib import Path

import requests
import rich.progress

from ..util import get_free_filename, extract_filename, extract_content_size


__all__ = ['handle_download']


# todo: catch errors
def handle_download(response: requests.Response, progress: rich.progress.Progress, canceled: threading.Event,
                    overwrite: bool) -> None:
    filename: str = extract_filename(response)
    if not overwrite:
        filename: str = get_free_filename(filename)

    filepath: Path = Path(filename)
    filepath.touch()  # ensure it exist for other threads/downloads
    tmpfile: Path = filepath.with_stem(f".{filepath.stem}")
    task_id: rich.progress.TaskID\
        = progress.add_task(description=filepath.name, start=True, total=extract_content_size(response))

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
