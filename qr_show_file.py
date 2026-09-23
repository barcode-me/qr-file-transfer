#!/usr/bin/env python3
"""Read a file as bytes and display its contents as a QR code."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

import cv2
from qrcode.exceptions import DataOverflowError

from qr_transfer_qr import encode_qr_bgr


logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

WINDOW_NAME = "QR from file (q or Esc to quit)"
MAX_QR_BINARY_BYTES = 2953


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Display the raw byte stream of a file as a QR code."
    )
    parser.add_argument("file", type=Path, metavar="FILE", help="File to encode")
    args = parser.parse_args()

    try:
        payload = args.file.read_bytes()
    except OSError as exc:
        logger.error("Could not read %s: %s", args.file, exc)
        return 1

    if len(payload) > MAX_QR_BINARY_BYTES:
        logger.error(
            "File is too large to fit in a single QR code: %s (%d bytes; maximum is %d)",
            args.file,
            len(payload),
            MAX_QR_BINARY_BYTES,
        )
        return 1

    try:
        qr_bgr = encode_qr_bgr(payload)
    except (DataOverflowError, ValueError):
        logger.error(
            "File is too large to fit in a single QR code: %s (%d bytes)",
            args.file,
            len(payload),
        )
        return 1

    logger.info("QR code ready. Press q to exit.")
    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
    cv2.imshow(WINDOW_NAME, qr_bgr)

    try:
        while cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) >= 1:
            if cv2.waitKey(50) & 0xFF in (ord("q"), 27):
                break
    finally:
        cv2.destroyAllWindows()

    return 0


if __name__ == "__main__":
    sys.exit(main())
