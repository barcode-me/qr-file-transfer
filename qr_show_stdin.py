#!/usr/bin/env python3
"""Read text from standard input and display it as a QR code."""

from __future__ import annotations

import logging
import sys

import cv2
from qrcode.exceptions import DataOverflowError

from qr_transfer_qr import make_qr_bgr


logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

WINDOW_NAME = "QR from stdin (q or Esc to quit)"


def main() -> int:
    logger.info("Enter the text to encode, then press Ctrl+D to end the input stream.")
    payload = sys.stdin.read()
    if not payload:
        logger.error("No input received on standard input")
        return 1

    try:
        qr_bgr = make_qr_bgr(payload)
    except DataOverflowError:
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
