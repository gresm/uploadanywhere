"""
Find WSGI file.
"""
from __future__ import annotations

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
