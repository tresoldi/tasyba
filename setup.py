"""
setup.py for the `tasyba` packager

Requirements are listed in `requirements.txt`.
"""


# Import Python standard libraries
from setuptools import setup, find_packages
from pathlib import Path
import glob

# The directory containing this file
LOCAL_PATH = Path(__file__).parent

# Build (recursive) list of resource files
# TODO: read from MANIFEST.in?
resource_files = []
for filename in glob.glob(str(Path("templates") / "*" / "*"), recursive=True):
    resource_files.append(filename)

# The text of the README file
README_FILE = (LOCAL_PATH / "README.md").read_text(encoding="utf-8")

# Load requirements, so they are listed in a single place
with open("requirements.txt", encoding="utf-8") as fp:
    install_requires = [dep.strip() for dep in fp.readlines()]

# This call to setup() does all the work
setup(
    author="Tiago Tresoldi",
    author_email="tiago.tresoldi@lingfil.uu.se",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries",
    ],
    data_files=resource_files,
    description="A set of tools for managing and deploying tabular data",
    extras_require={
        "dev": ["black", "flake8", "twine", "wheel"],
        "test": ["pytest"],
    },
    include_package_data=True,
    install_requires=install_requires,
    keywords=["tabular data", "csv", "tsv", "fair data"],
    license="GPLv3",
    long_description=README_FILE,
    long_description_content_type="text/markdown",
    name="tasyba",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.6",
    test_suite="tests",
    tests_require=[],
    url="https://github.com/tresoldi/tasyba",
    version="0.1.0",  # remember to sync with __init__.py
    zip_safe=False,
)
