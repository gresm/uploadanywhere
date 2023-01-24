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
"""BaseFinder is an abstract class for different finders."""
from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path as _Path
import sys

from .tools import test_path, warning, if_test, error

class BaseFinder(ABC):
    """Base class for the finders."""

    DEFAULT_SEARCH_DIR: _Path | None = None

    searching_for: str = ""
    searching_for_file: bool = False

    test_path = staticmethod(test_path)
    warning = staticmethod(warning)
    if_test = staticmethod(if_test)
    error = staticmethod(error)

    def __init__(self, path: _Path | None = None, search_dir: _Path | None = None):
        self.path = path
        self.search_dir =  search_dir or self.DEFAULT_SEARCH_DIR

    def found(self):
        """Return True if found found, False otherwise."""
        return self.path is not None

    @classmethod
    def get_possible_from_dir(cls, path: _Path, list_dirs: bool = False):
        """Get possible files in path."""

        possible = []

        for possible_path in path.iterdir():
            if (list_dirs and path.is_dir()) or (not list_dirs and path.is_file()):
                possible.append(possible_path)

        return possible

    def select_file_from_dir(self, path: _Path, is_dir: bool = False):
        """Select file from directory."""
        if self.found():
            return

        select = self.get_possible_from_dir(path, is_dir)

        if len(select) == 0:
            self.warning(f"Searched directory '{str(path)}' doesn't contain any valid entries.")
            self.manual_selection()
        elif len(select) == 1:
            if self.if_test(f"Use {str(select[0])}?"):
                self.path = select[0]
            else:
                self.manual_selection()

        print(f"Select a {self.searching_for} from the list:")
        for idx, path in enumerate(select, 1):
            print(f"[{idx}] {str(path)}")

        str_num = input("Type number, next to the path, or nothing for manual configuration: ")

        if not str_num:
            self.manual_selection()
            return

        if not str_num.isdigit():
            self.error("Not a number.")

        selection = int(str_num)
        if not 0 < selection <= len(select):
            error("Invalid index.")

        self.path = select[selection]

    @abstractmethod
    def find(self):
        """Find through interactive console"""

    def manual_selection(self):
        """Manually select file path."""

        if self.found():
            return

        if self.if_test("Proceed with manual configuration?"):
            path = _Path(input(f"Enter valid path for {self.searching_for}: "))
            self.test_path(path, self.searching_for_file)
            self.path = path
        else:
            sys.exit(0)
