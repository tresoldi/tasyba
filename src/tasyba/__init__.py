"""
tasyba __init__.py file
"""

# Package metadata
__version__ = "0.1.0"  # remember to update setup.py
__author__ = "Tiago Tresoldi"
__email__ = "tiago.tresoldi@lingfil.uu.se"

# Import modules
from .common import read_tabular, load_config
from .render import render_database


def caller(filepath):
    # Read and parse configuration file
    config, replaces = load_config(filepath)

    # Read the data
    # TODO: fix for multiple tables and metadata
    data = {}
    data["single"] = read_tabular(config["source"])

    # If the `config` does not specify the columns to use, use all of them
    # TODO: move this logic to configuration reading/parsing
    if "single_table" not in config:
        config["single_table"] = list(data["single"][0].keys())

    # Build list of table replaces (for header, mostly)
    table_names = [key for key in config if key.endswith("_table")]
    tables = []
    for tname in table_names:
        label = tname.split("_")[0]
        tables.append({"name": label.capitalize(), "url": f"{label}.html"})

    # Build site
    render_database(data, replaces, tables, config)


# Build the package namespace
__all__ = ["read_tabular", "load_config", "render_database", "caller"]
