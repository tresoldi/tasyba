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
from .common import read_tabular
from .fl import describe_resource
from .render import render_database, load_template, build_html_table
from .script import load_makefile, run_makefile


def caller(filepath):
    # TODO: move to header when moving to its own module
    from frictionless import Package

    # Read and parse configuration file
    config = load_makefile(filepath)

    # Iterate over the steps
    package = Package()
    tables = {}
    for entry in config["steps"]:
        # Obtain a tuple representation of the entry, from where we draw the command and
        # its arguments, making it easier to later move to a programming-language-like
        # interface
        command, args = tuple(entry.items())[0]

        if command == "describe_resource":
            # Describe a resource
            resource = describe_resource(args["source"])

            # Store the resource if requested
            # TODO: check if the name is already taken, have a flag to overwrite
            if "write" in args:
                resource.to_yaml(args["write"])

        elif command == "add_resource":
            # Add a resource to the package; if we point to a YAML file,
            # we assume it is a frictionless resource description; otherwise,
            # we assume it is a path to a raw data file (tabular, Excel,
            # JSON, etc.), which must be loaded via a frictionless resource
            # description

            # Load data
            table_name = args.get("name", Path(args["source"]).stem)
            tables[table_name] = read_tabular(args["source"])
        elif command == "field_remove":
            # Remove fields
            # TODO: move to frictionless
            for row in tables[args["table"]]:
                for field in args["fields"]:
                    del row[field]
        elif command == "table_deploy":
            # Build replacement dictionary; which for future expansions it is
            # preferable to keep separate from the actual configuration while
            # using a single file not to scare potential users with too much
            # structure to learn. Remember that, in order to make
            # deployment easy, we are being quite strict here in terms of
            # templates, etc.
            replaces = {
                "title": args["title"],
                "description": args["description"],
                "author": args["author"],
                "favicon": args["favicon"],
                "mainlink": args["mainlink"],
                "citation": args["citation"],
            }

            # Load Jinja2 template
            template_env = load_template(args)

            # Render table as HTML
            build_html_table(args["table"], tables, replaces, template_env)


# Build the package namespace
__all__ = ["read_tabular", 
"run_makefile",
"load_makefile", "load_template", "render_database", "caller"]
