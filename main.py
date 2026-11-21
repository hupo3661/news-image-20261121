#!/usr/bin/env python3
"""Ship the pre-rendered 21 November 2026 world-news image.

The infographic (entry.png, 1024x1024) sits beside this file; it was
drawn ahead of time by render.py. This program's only job is to put
an exact copy of it at $MAKEFUN_OUTPUT_DIR/entry.png (or
/output/entry.png when that variable is unset).

Determinism: the copy is written through a temporary file and moved
into place atomically, and the delivered file is hashed and compared
against the bundled original before the program reports success.
No network, no clock, no randomness — two runs write identical bytes.
"""

import hashlib
import os
import sys
from pathlib import Path

IMAGE_NAME = "entry.png"
CHUNK = 1 << 16


def sha256_of(path):
    """Hex SHA-256 digest of a file, streamed in chunks."""
    hasher = hashlib.sha256()
    with open(path, "rb") as stream:
        while True:
            block = stream.read(CHUNK)
            if not block:
                break
            hasher.update(block)
    return hasher.hexdigest()


class Deliverer:
    """Copies the bundled image to the output directory, verified."""

    def __init__(self):
        here = Path(__file__).resolve().parent
        self.bundled = here / IMAGE_NAME
        out_root = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
        self.target = Path(out_root) / IMAGE_NAME

    def check_bundled(self):
        if not self.bundled.is_file():
            sys.exit(
                "error: %s not found next to main.py "
                "(looked in %s)" % (IMAGE_NAME, self.bundled.parent)
            )

    def deliver(self):
        """Write via a temp file, swap in atomically, verify the hash."""
        self.check_bundled()
        self.target.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.target.with_name(self.target.name + ".tmp")
        with open(self.bundled, "rb") as src, open(tmp, "wb") as dst:
            while True:
                block = src.read(CHUNK)
                if not block:
                    break
                dst.write(block)
        os.replace(tmp, self.target)

        wanted = sha256_of(self.bundled)
        got = sha256_of(self.target)
        if self.target.stat().st_size != self.bundled.stat().st_size:
            sys.exit(
                "error: delivered %s has the wrong size "
                "(%d bytes, expected %d)"
                % (
                    self.target,
                    self.target.stat().st_size,
                    self.bundled.stat().st_size,
                )
            )
        if got != wanted:
            sys.exit(
                "error: delivered %s failed verification "
                "(sha256 %s, expected %s)" % (self.target, got, wanted)
            )
        size = self.target.stat().st_size
        print(
            "delivered %s (%d bytes, sha256 %s)"
            % (self.target, size, wanted)
        )


def main():
    Deliverer().deliver()


if __name__ == "__main__":
    main()
