# -*- coding=utf-8 -*-
r"""

"""
import typing as t


__all__ = ['__cmd__']


def __cmd__(source: str, dimensions: str, output: str,
            yes: bool, thumbnail: bool, new_mode: t.Optional[str], save_args: t.List[t.Tuple[str, t.Any]]):
    r"""
    img resize input.png --thumbnail 1000x1000 output.png
    """
    from pathlib import Path
    from PIL import Image  # note: Pillow is installed into the archive
    from ..util import split_dimensions

    output = Path(output)
    if output.exists():
        if not output.is_file():
            raise RuntimeError(f'Output "{output!s}" does exist but is not a file.')
        if not yes:
            raise FileExistsError(f'Output file "{output!s}" already exists.')

    size = split_dimensions(dimensions)

    with Image.open(source) as image:
        if thumbnail:
            image.thumbnail(size=size, resample=Image.Resampling.LANCZOS)
        else:
            image = image.resize(size=size, resample=Image.Resampling.LANCZOS)
        if new_mode is not None:
            image = image.convert(mode=new_mode)
        image.save(output, **dict(save_args))
