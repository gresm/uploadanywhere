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
import sys
import os


try:
    from uploadanywhere.cli import error, warning, if_test, test_path
except ImportError:
    print("Package 'uploadanywhere' not found. Running automatic installment")
    if os.system("pip install git+https://github.com/gresm/uploadanywhere@main") != 0:
        print("Instalation script returned with non-zero code, aborting.")
        sys.exit(1)
    try:
        from uploadanywhere.cli import error, warning, if_test, test_path
    except ImportError:
        print("Failed to import 'uploadanywhere' after installation, "
              "try eiter running this script again or installing 'uploadanywhere' manually")
        sys.exit(1)
    print("Instalation succesfull, continuing with setup script.")

from git.repo import Repo


wsgi_dir = Path("/var/www")
proj_home = Path("/home")
wsgi_path: Path | None = None
proj_path: Path | None = None

git_repo: Repo | None = None


def _wsgi_manual_config():
    if if_test("Proceed with manual configuration?"):
        globals()["wsgi_path"] = Path(input("Enter valid path for wsgi python file: "))
        test_path(wsgi_path, True)
    else:
        sys.exit(0)


print("Searching for WSGI file to patch.")
if not wsgi_dir.exists():
    warning("WSGI setup files folder not found.")
    _wsgi_manual_config()

if wsgi_path is None:
    possible = []

    for possible_path in wsgi_dir.iterdir():
        if possible_path.is_file() and possible_path.suffix == ".py":
            possible.append(possible_path)

    if len(possible) == 0:
        warning("WSGI default setup folder empty.")
        _wsgi_manual_config()
    elif len(possible) == 1:
        if if_test(f"Use {str(possible[0])}?"):
            wsgi_path = possible[0]
        else:
            _wsgi_manual_config()

    print("Possible files:")
    for idx, file in enumerate(possible):
        print(f"[{idx + 1}] {str(file)}")

    option = input("Select file number, or nothing for manual configuration: ")
    if not option:
        _wsgi_manual_config()
    else:
        if option.isdigit():
            opt = int(option)
            if not 0 < opt <= len(possible):
                error("Invalid index.")
            wsgi_path = possible[opt]
        else:
            error("Not a number.")


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

setup_post_commit_hook = if_test("Setup post-commit hook?")
