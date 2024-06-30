# -*- coding=utf-8 -*-
r"""

"""
import typing as t
from .._typing import T_DIMENSIONS


__all__ = ['__cmd__']


def __cmd__(source: str, output: str,
            yes: bool, mode: t.Optional[str], save_args: t.List[t.Tuple[str, t.Any]],
            thumbnail: t.Optional[T_DIMENSIONS], size: t.Optional[T_DIMENSIONS]):
    r"""
    img repack input.png output.png --thumbnail 1000x1000
    """
    from pathlib import Path
    from PIL import Image  # note: Pillow is installed into the archive

    output = Path(output)
    if output.exists():
        if not output.is_file():
            raise RuntimeError(f'Output "{output!s}" does exist but is not a file.')
        if not yes:
            raise FileExistsError(f'Output file "{output!s}" already exists.')

    with Image.open(source) as image:
        if thumbnail is not None:
            image.thumbnail(size=size, resample=Image.Resampling.LANCZOS)
        elif size is not None:
            new_size = get_size(new_size=size, image_size=image.size)
            image = image.resize(size=new_size, resample=Image.Resampling.LANCZOS)

        if mode is not None:
            image = image.convert(mode=mode)

        image.save(output, **dict(save_args))


def get_size(new_size: T_DIMENSIONS, image_size: T_DIMENSIONS) -> T_DIMENSIONS:
    r"""
    allows to pass -1 for width xor height to keep aspect

    e.g. -1x480 to resize to 480p

    :param new_size: new specified size
    :param image_size: old image size
    :return:
    """
    width, height = new_size

    if width == -1 == height:
        raise ValueError("either width or height can be -1 to keep the aspect. not both")
    elif width == -1:
        width = round(height * (image_size[0] / image_size[1]))
    elif height == -1:
        height = round(width * (image_size[1] / image_size[0]))

    return width, height
