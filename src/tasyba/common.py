"""
Common functions for the TASYBA project.
"""

# Import Python standard libraries
from pathlib import Path
from typing import *
import csv

# Import 3rd-party libraries
import chardet
import yaml


def read_tabular(filename: Union[Path, str]) -> List[Dict[str, str]]:
    """
    Reads a tabular file and returns its contents as list of dictionaries.

    The function will automatically detect the delimiter used in the file
    using the `csv.Sniffer` functionality,
    as well as the character encoding using the `chardet` library. The first
    row of the file will be used as a header to provide the keys for the
    dictionaries.

    Parameters
    ----------
    filename : Union[Path,str]
        The path to the file to read.

    Returns
    -------
    List[Dict[str,str]]
        The contents of the tabular file as a list of dictionaries.
    """

    # Read file to detect encoding and delimiter
    with open(filename, "rb") as handler:
        raw = handler.read()
        encoding = chardet.detect(raw)["encoding"]
        dialect = csv.Sniffer().sniff(raw.decode(encoding))

    # Read file with detected encoding and delimiter
    with open(filename, encoding=encoding) as handler:
        reader = csv.DictReader(handler, dialect=dialect)
        data = [row for row in reader]

    return data


