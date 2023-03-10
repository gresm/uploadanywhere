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
Utility for finding project location.
"""

from __future__ import annotations

from pathlib import Path as _Path

from .base_finder import BaseFinder


DEFAULT_PROJECTS_DIR = _Path("/home")


class ProjectFinder(BaseFinder):
    """Project Finder class"""

    searching_for = "project directory"
    searching_for_file = False
    DEFAULT_SEARCH_DIR = DEFAULT_PROJECTS_DIR

    def _find(self):
        print("Selecting project.")
        if self.if_test("Use default project layout?"):
            self.select_from_dir(self.DEFAULT_SEARCH_DIR, True)
            self.path = self.path / "mysite"
            self.test_path(self.path, False)
        else:
            self.manual_selection()
