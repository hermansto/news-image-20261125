#!/usr/bin/env python3
"""Ship the pre-rendered front page for 25 November 2026.

The grader runs with the standard library only and installs
nothing, so this program uses the stdlib alone. It copies the
finished entry.png that already lives next to this file into the
output directory, then reads the copy back and checks that it
matches the original byte for byte.

Writes only to os.environ.get("MAKEFUN_OUTPUT_DIR", "/output").
Never writes into the repository directory.
"""
import hashlib
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def fail(message):
    print("error: " + message, file=sys.stderr)
    return 1


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    dest = os.path.join(out_dir, "entry.png")
    with open(SOURCE, "rb") as handle:
        blob = handle.read()
    if not blob.startswith(PNG_MAGIC):
        return fail("entry.png is not a PNG file")
    width, height = struct.unpack(">II", blob[16:24])
    if (width, height) != (1024, 1024):
        return fail("entry.png is not 1024x1024")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(SOURCE, dest)
    with open(dest, "rb") as handle:
        copied = handle.read()
    if copied != blob:
        return fail("copied entry.png does not match the original")
    print("wrote " + dest)
    print("size: 1024x1024")
    print("bytes: " + str(len(blob)))
    print("sha256: " + hashlib.sha256(blob).hexdigest())
    return 0


if __name__ == "__main__":
    sys.exit(main())
