"""
tasyba __init__.py file
"""

# Package metadata
__version__ = "0.1.0"  # remember to update setup.py
__author__ = "Tiago Tresoldi"
__email__ = "tiago.tresoldi@lingfil.uu.se"

# Import Python standard libraries
from pathlib import Path  # TODO: drop when moving to frictionless

# Import modules
from .common import read_tabular, load_config
from .render import render_database, load_template, build_html_table


def caller(filepath):
    # Read and parse configuration file
    config = load_config(filepath)

    # Iterate over the steps
    tables = {}
    for step in config["steps"]:
        if "load" in step:
            # Load data
            table_name = step.get("name", Path(step["source"]).stem)
            tables[table_name] = read_tabular(step["source"])
        elif "field_remove" in step:
            # Remove fields
            # TODO: move to frictionless
            for row in tables[step["table"]]:
                for field in step["fields"]:
                    del row[field]
        elif "table_deploy" in step:
            # Build replacement dictionary; which for future expansions it is
            # preferable to keep separate from the actual configuration while
            # using a single file not to scare potential users with too much
            # structure to learn. Remember that, in order to make
            # deployment easy, we are being quite strict here in terms of
            # templates, etc.
            replaces = {
                "title": step["title"],
                "description": step["description"],
                "author": step["author"],
                "favicon": step["favicon"],
                "mainlink": step["mainlink"],
                "citation": step["citation"],
            }

            # Load Jinja2 template
            template_env = load_template(step)

            # Render table as HTML
            build_html_table(step["table"], tables, replaces, template_env)


# Build the package namespace
__all__ = ["read_tabular", "load_config", "load_template", "render_database", "caller"]
