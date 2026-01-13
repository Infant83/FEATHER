#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Compatibility wrapper for the in-package report CLI.
"""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if SRC.exists():
    sys.path.insert(0, str(SRC))

from federlicht.report import main  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(main())
