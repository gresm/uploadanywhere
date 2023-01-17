"""Command line utilities for "uploadanywhere" package."""

import sys
from pathlib import Path


try:
    from colorama import Back as _Back
    RED = _Back.RED
    RESET = _Back.RESET
    YELLOW = _Back.YELLOW
except ImportError:
    RED = ""
    RESET = ""
    YELLOW = ""


def error(err, exit=True):
    """Print error."""
    print(f"{RED}ERROR:{RESET} {err}", sys.stderr)
    if exit:
        sys.exit(1)


def warning(warn):
    """Print warning."""
    print(f"{YELLOW}WARNING:{RESET} {warn}", sys.stderr)


def if_test(inp):
    """Test if user wants to."""
    return input(f"{inp} (y/n): ") in {"y", "yes", "Y", "YES"}


def test_path(path: Path, is_file):
    """Test if path is valid"""
    if not path.exists():
        error(f"Invalid path '{str(path)}'")
    if path.is_file():
        if not is_file:
            error(f"Path '{str(path)}' is a file.")
    elif is_file:
        error(f"Path '{str(path)}' is not a file.")
