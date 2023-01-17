"""Setup uploadanywhere"""
from pathlib import Path
from setuptools import setup


long_description = Path("README.md").read_text("utf-8")
requirements = Path("requirements.txt").read_text("utf-8").splitlines()


setup(
    name="uploadanywhere",
    description="Utility to setup git projects on pythonanywhere.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="gresm",
    url="https://github.com/gresm/uploadanywhere",
    packages=["uploadanywhere"],
    package_dir={"uploadanywhere": "uploadanywhere"},
    install_requires=requirements
)
