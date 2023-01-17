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

"""
Find WSGI file.
"""
from __future__ import annotations


__all__ = [
    "WSGI_DEFAULT_DIR",
    "WSGIFinder"
]


from pathlib import Path as _Path
import sys

from .tools import test_path, warning, if_test, error


WSGI_DEFAULT_DIR = _Path("/var/www")


class WSGIFinder:
    """WSGI Finder class"""

    def __init__(self, wsgi_dir: _Path | None = None):
        self.file: _Path | None = None
        self.wsgi_dir = wsgi_dir or WSGI_DEFAULT_DIR

    def found(self):
        """Return True if WSGI file found, False otherwise."""
        return self.file is not None

    def manual_selection(self):
        """Manually select wsgi file path."""

        if self.found():
            return

        if if_test("Proceed with manual configuration?"):
            path = _Path(input("Enter valid path for wsgi python file: "))
            test_path(path, True)
            self.file = path
        else:
            sys.exit(0)

    def select_from_dir(self):
        """Choose between files in wsgi directory"""

        if self.found():
            return

        possible = []

        for possible_path in self.wsgi_dir.iterdir():
            if possible_path.is_file() and possible_path.suffix == ".py":
                possible.append(possible_path)

        if len(possible) == 0:
            warning("WSGI default setup folder empty.")
            self.manual_selection()
        elif len(possible) == 1:
            if if_test(f"Use {str(possible[0])}?"):
                self.file = possible[0]
            else:
                self.manual_selection()

        print("Possible files:")
        for idx, file in enumerate(possible):
            print(f"[{idx + 1}] {str(file)}")

        option = input("Select file number, or nothing for manual configuration: ")
        if not option:
            self.manual_selection()
        else:
            if option.isdigit():
                opt = int(option)
                if not 0 < opt <= len(possible):
                    error("Invalid index.")
                self.file = possible[opt]
            else:
                error("Not a number.")


    def find(self):
        """Find wsgi file"""
        print("Searching for WSGI file to patch.")
        if not self.wsgi_dir.exists():
            warning("WSGI setup files folder not found.")
            self.manual_selection()
        self.select_from_dir()
        return self.file
