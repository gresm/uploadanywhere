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
Utility to configure pythonanywhere with github.
"""
from __future__ import annotations
from pathlib import Path

from git.repo import Repo

try:
    from .tools import if_test, test_path, error
    from .wsgi_finder import WSGIFinder
except ImportError:
    from uploadanywhere.cli.tools import if_test, test_path, error
    from uploadanywhere.cli.wsgi_finder import WSGIFinder


def main():
    """Main cli function"""

    # wsgi_dir = Path("/var/www")
    proj_home = Path("/home")
    # wsgi_path: Path | None = None
    proj_path: Path | None = None
    git_repo: Repo | None = None

    find_wsgi = WSGIFinder()
    wsgi_path = find_wsgi.find()

    if wsgi_path is None:
        error("Unknown error, WSGI file not found.")

    test_path(wsgi_path, True)

    print("Selecting project.")
    if if_test("Use default project layout?"):
        proj_name = input("Enter project name: ")
        proj_path = proj_home / proj_name / "mysite"
        test_path(proj_path, False)
    else:
        proj_path = Path(input("Enter project path: "))
        test_path(proj_path, False)

    repo_url = input("Enter git repository url: ")
    if if_test("Clone the repository?"):
        git_repo = Repo.clone_from(repo_url, proj_path)
    else:
        git_repo = Repo(proj_path)

    setup_post_commit_hook = if_test("Setup local post-commit hook?")


if __name__ == "__main__":
    main()
