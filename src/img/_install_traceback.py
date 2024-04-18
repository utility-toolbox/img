# -*- coding=utf-8 -*-
r"""

"""
try:
    import runpy
    import rich.traceback

    rich.traceback.install(show_locals=True, suppress=[runpy])
except ModuleNotFoundError:
    pass
