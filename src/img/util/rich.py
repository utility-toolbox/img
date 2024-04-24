# -*- coding=utf-8 -*-
r"""

"""


__all__ = ['get_progress_columns']


def get_progress_columns():
    import rich.progress
    yield rich.progress.TextColumn("[progress.description]{task.description}")
    yield rich.progress.BarColumn(bar_width=None)
    yield rich.progress.TimeElapsedColumn()
    yield rich.progress.TimeRemainingColumn(compact=True)
    yield rich.progress.TextColumn("|")
    yield rich.progress.FileSizeColumn()
    yield rich.progress.TextColumn("/")
    yield rich.progress.TotalFileSizeColumn()
    yield rich.progress.TextColumn("|")
    yield rich.progress.TransferSpeedColumn()
