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
Utility for finding WSGI file.
"""
from __future__ import annotations


__all__ = [
    "WSGI_DEFAULT_DIR",
    "WSGIFinder"
]


from pathlib import Path as _Path


from .base_finder import BaseFinder


WSGI_DEFAULT_DIR = _Path("/var/www")


class WSGIFinder(BaseFinder):
    """WSGI Finder class"""

    DEFAULT_SEARCH_DIR = WSGI_DEFAULT_DIR

    searching_for = "wsgi file"
    searching_for_file = True

    def find(self):
        """Find wsgi file"""
        print("Searching for WSGI file to patch.")
        if not self.search_dir.exists():
            self.warning("WSGI setup files folder not found.")
            self.manual_selection()
        self.select_file_from_dir(self.search_dir, False)
        return self.path
