"""
tasyba __init__.py file
"""

# Package metadata
__version__ = "0.1.0"  # remember to update setup.py
__author__ = "Tiago Tresoldi"
__email__ = "tiago.tresoldi@lingfil.uu.se"

# Import modules
from .common import read_tabular

# Build the package namespace
__all__ = ["read_tabular"]
