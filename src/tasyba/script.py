"""
Module with functions for running the script-like commands.
"""

# Import Python standard libraries
from typing import *
from pathlib import Path

# Import 3rd-party libraries
from frictionless import Package, Resource, transform, steps
import yaml

# Import other modules
from tasyba.fl import describe_resource


def run_makefile(config: Dict[str, Any]) -> None:
    """
    Runs a database configuration script.

    Parameters
    ----------
    config : Dict[str,Any]
        The configuration script to run.
    """

    # Instantiate a frictionless package to hold the resources
    package = Package(resources=[])

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
            # description.
            # TODO: derive name if missing, or leave to frictionless?
            if Path(args["source"]).suffix == ".yaml":
                package = transform(
                    package,
                    steps=[
                        steps.resource_add(
                            Resource(
                            "/home/tiagot/repos/tasyba/tests/data/"+args["source"],
                            #path="/home/tiagot/repos/tasyba/tests/data/",
                                trusted=True,
                            )#, base_path="/home/tiagot/repos/tasyba/tests/data/"

                        )
                    ]
                )
            else:
                target = transform(
                    package,
                    steps=[steps.resource_add(name=args["name"], path=args["source"])],
                )
        else:
            # Fallback
            raise ValueError(f"Unknown command: {command}")


def load_makefile(filename: Union[Path, str]) -> Dict[str, Any]:
    """
    Reads a database configuration script from a YAML file.

    Parameters
    ----------
    filename : Union[Path,str]
        The path to the configuration YAML file to read.

    Returns
    -------
    Dict[str,Any]
        The contents of the configuration file as a dictionary.
    """

    # Read file
    with open(filename, "r", encoding="utf-8") as handler:
        config = yaml.load(handler, Loader=yaml.FullLoader)

    # TODO: validate the script, making sure all mandatory fields are present, etc.

    return config
