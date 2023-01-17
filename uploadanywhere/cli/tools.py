# MIT License

# Copyright (c) 2023 gresm

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Command line utilities for "uploadanywhere" package."""


__all__ = [
    "error",
    "warning",
    "if_test",
    "test_path"
]


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
        # This should never happen.
        RED = ""
        RESET = ""
        YELLOW = ""
    else:
        RED = "\033[31m"
        RESET = "\033[39m"
        YELLOW = "\033[33m"


def error(err, do_exit=True):
    """Print error."""
    print(f"{RED}ERROR:{RESET} {err}", file=sys.stderr)
    if do_exit:
        sys.exit(1)


def warning(warn):
    """Print warning."""
    print(f"{YELLOW}WARNING:{RESET} {warn}", file=sys.stderr)


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
