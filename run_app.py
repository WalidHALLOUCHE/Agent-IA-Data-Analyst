"""Convenience launcher for the Streamlit application."""

from __future__ import annotations

import subprocess
import sys


def main() -> None:
    command = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        "app/main.py",
        "--server.address=0.0.0.0",
        "--server.port=8501",
    ]
    raise SystemExit(subprocess.call(command))


if __name__ == "__main__":
    main()

