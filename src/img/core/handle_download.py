# -*- coding=utf-8 -*-
r"""

"""
import typing as t
import threading
from pathlib import Path

if t.TYPE_CHECKING:
    import requests
    import rich.progress

from ..util import get_free_filename, extract_filename, extract_content_size
from ..constants import FileConflictStrategy


__all__ = ['handle_download']


def handle_download(response: 'requests.Response', head: t.Optional[bytes], progress: 'rich.progress.Progress',
                    canceled: 'threading.Event', on_conflict: 'FileConflictStrategy') -> None:
    import rich.progress
    from rich.markup import escape

    filepath: Path = Path(extract_filename(response))
    tmpfile: Path = filepath.with_stem(f".{filepath.stem}")
    if filepath.exists():
        if on_conflict is FileConflictStrategy.skip:
            progress.console.print(f"[gray]Skipping {escape(response.url)} as {escape(filepath.name)} already exists[/]")
            return  # cancel download
        elif on_conflict is FileConflictStrategy.rename:
            filepath = Path(get_free_filename(filepath))
            filepath = filepath.with_name(get_free_filename(filepath.name))
            tmpfile: Path = filepath.with_stem(f".{filepath.stem}")
        # elif on_conflict is FileConflictStrategy.replace:
        #     pass  # no need for this

    task_id: rich.progress.TaskID\
        = progress.add_task(description=filepath.name, start=True, total=extract_content_size(response))

    with open(tmpfile, 'wb') as file:
        if head:
            file.write(head)
        for chunk in response.iter_content(chunk_size=1024*10):
            if canceled.is_set():
                tmpfile.unlink(missing_ok=True)  # is this a problem with file.close()?
                return
            progress.update(task_id, advance=len(chunk))
            file.write(chunk)

    filepath.unlink(missing_ok=True)  # remove old
    tmpfile.rename(filepath)  # tmpfile -> file
    progress.remove_task(task_id)  # remove now unnecessary progress bar
    progress.console.print(f"{escape(filepath.name)} is done")  # but keep a log
