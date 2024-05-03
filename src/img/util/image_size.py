# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        get_image_size
# Purpose:     extract image dimensions given a file path using just
#              core modules
#
# Author:      Paulo Scardine (based on code from Emmanuel VAÏSSE)
#
# Created:     26/09/2013
# Copyright:   (c) Paulo Scardine 2013
# Licence:     MIT
# -------------------------------------------------------------------------------
# https://stackoverflow.com/questions/15800704/get-image-size-without-loading-image-into-memory
# https://raw.githubusercontent.com/scardine/image_size/master/get_image_size.py
import io
import struct
import typing as t


__all__ = ['UnknownImageFormatError', 'get_image_size']


class UnknownImageFormatError(Exception):
    pass


def get_image_size(content: t.Union[t.BinaryIO, bytes]):
    """
    Return (width, height) for a given img file content - no external
    dependencies except the os and struct modules from core
    """
    # size = os.path.getsize(file_path)
    #
    # with open(file_path) as file:
    #     height = -1
    #     width = -1
    #     data = file.read(25)

    if isinstance(content, bytes):
        data = content
        content = io.BytesIO(data)
    else:
        data: bytes = content.read(25)

    total = len(data)

    if (total >= 10) and data[:6] in (b'GIF87a', b'GIF89a'):
        # GIFs
        w, h = struct.unpack("<HH", data[6:10])
        width = int(w)
        height = int(h)
    elif ((total >= 24) and data.startswith(b'\211PNG\r\n\032\n')
          and (data[12:16] == b'IHDR')):
        # PNGs
        w, h = struct.unpack(">LL", data[16:24])
        width = int(w)
        height = int(h)
    elif (total >= 16) and data.startswith(b'\211PNG\r\n\032\n'):
        # older PNGs?
        w, h = struct.unpack(">LL", data[8:16])
        width = int(w)
        height = int(h)
    elif (total >= 2) and data.startswith(b'\377\330'):
        # JPEG
        msg = " raised while trying to decode as JPEG."
        content.seek(0)
        content.read(2)
        b = content.read(1)
        try:
            w, h = -1, -1
            while b and ord(b) != 0xDA:
                while ord(b) != 0xFF:
                    b = content.read(1)
                while ord(b) == 0xFF:
                    b = content.read(1)
                if 0xC0 <= ord(b) <= 0xC3:
                    content.read(3)
                    h, w = struct.unpack(">HH", content.read(4))
                    break
                else:
                    content.read(int(struct.unpack(">H", content.read(2))[0]) - 2)
                b = content.read(1)
            width = int(w)
            height = int(h)
        except struct.error:
            raise UnknownImageFormatError("StructError" + msg)
        except ValueError:
            raise UnknownImageFormatError("ValueError" + msg)
        except Exception as e:
            raise UnknownImageFormatError(e.__class__.__name__ + msg)
    elif (total >= 4) and data.startswith(b'RIFF'):  # WEBP
        r"""
        https://datatracker.ietf.org/doc/html/rfc6386 (search for 'width' and the first describes this)

       Start code byte 0     0x9d
       Start code byte 1     0x01
       Start code byte 2     0x2a

       16 bits      :     (2 bits Horizontal Scale << 14) | Width (14 bits)
       16 bits      :     (2 bits Vertical Scale << 14) | Height (14 bits)
        """
        content.seek(0)
        head = content.read(128)  # dunno with size
        start = head.find(b'\x9d\x01\x2a')
        if start == -1:
            raise UnknownImageFormatError("size-bytes for .webp not found")
        fmt = "<HH"
        width, height = struct.unpack(fmt, head[start + 3:start + 3 + struct.calcsize(fmt)])
    else:
        raise UnknownImageFormatError(
            "Sorry, don't know how to get information from this format."
        )

    return width, height
