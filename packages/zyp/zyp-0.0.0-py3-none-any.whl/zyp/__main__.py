"""Support executing the CLI by doing `python -m zyp`."""
from __future__ import annotations

from zyp.cli import cli

if __name__ == "__main__":
    raise SystemExit(cli())
