# -*- coding=utf-8 -*-
r"""

"""
import typing as t


__all__ = ['__cmd__']


def __cmd__(output: str, dimensions: str, images: t.List[str],
            yes: bool, save_args: t.List[t.Tuple[str, t.Any]]):
    r"""
    img merge -o output.jpg 2x1 left.jpg right.jpg
    """
    import statistics
    from pathlib import Path
    from contextlib import ExitStack
    from PIL import Image

    output = Path(output)
    if output.exists():
        if not output.is_file():
            raise RuntimeError(f'Output "{output!s}" does exist but is not a file.')
        if not yes:
            raise FileExistsError(f'Output file "{output!s}" already exists.')

    n_width, n_height = split_dimensions(dimensions)
    if len(images) != n_width * n_height:
        raise SyntaxError("Bad amount of images passed")

    with ExitStack() as stack:
        images: t.List[Image.Image] = [stack.enter_context(Image.open(src)) for src in images]

        average_width = round(statistics.mean((img.width for img in images)))
        average_height = round(statistics.mean((img.height for img in images)))

        images = [img.resize((average_width, average_height), resample=Image.Resampling.LANCZOS)
                  for img in images]

        total_width = n_width * average_width
        total_height = n_height * average_height

        with Image.new('RGBA', (total_width, total_height)) as image:
            for i, img in enumerate(images):
                x, y = int((i % n_width) * average_width), int((i // n_width) * average_height)
                image.paste(img, (x, y))
            image.save(output, **dict(save_args))


def split_dimensions(dimension: str) -> t.Tuple[int, int]:
    import re
    match = re.search(r'(\d+)x(\d+)', dimension)
    if match is None:
        raise ValueError(f'Invalid dimension: {dimension} (expected: 0x0)')
    return int(match.group(1)), int(match.group(2))
