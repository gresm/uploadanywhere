"""Command line utilities for "uploadanywhere" package."""

import sys
from pathlib import Path


try:
    from colorama import Fore as _Fore, just_fix_windows_console
    RED = _Fore.RED
    RESET = _Fore.RESET
    YELLOW = _Fore.YELLOW
    just_fix_windows_console()
except ImportError:
    # If colorama is not found.
    if sys.platform == "win32":
        RED = ""
        RESET = ""
        YELLOW = ""
    else:
        RED = "\033[31m"
        RESET = "\033[39m"
        YELLOW = "\033[33m"


def error(err, do_exit=True):
    """Print error."""
    print(f"{RED}ERROR:{RESET} {err}", sys.stderr)
    if do_exit:
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
