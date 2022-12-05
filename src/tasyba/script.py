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


def run_makefile(config: Dict[str, Any], basepath: Union[Path, str]) -> Package:
    """
    Runs a database configuration script.

    Parameters
    ----------
    config : Dict[str,Any]
        The contents of the configuration file as a dictionary.
    basepath : Union[Path,str]
        The base path to use for relative paths in the configuration file.

    Returns
    -------
    Package
        The package containing the resources created by the script.
    """

    # Have `basepath` as a Path object, to properly iterate with other resourcess
    if isinstance(basepath, str):
        basepath = Path(basepath)

    # Instantiate a frictionless package to hold the resources
    package = Package(resources=[], basepath=str(basepath))

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
                        steps.resource_add(Resource(str(basepath / args["source"])))
                    ],
                )
            else:
                package = transform(
                    package,
                    steps=[steps.resource_add(name=args["name"], path=args["source"])],
                )
        elif command == "remove_resource":
            # Remove a resource from the package
            package = transform(
                package, steps=[steps.resource_remove(name=args["name"])]
            )
        elif command == "table_print":  # TODO: rename to resource print?
            resource = package.get_resource(args["name"])
            transform(resource, steps=[steps.table_print()])
        elif command == "table_transpose":
            # Transpose a table: obtain the transposed table and replace the original,
            # by deleting the original and adding the transposed one
            resource = package.get_resource(args["name"])
            transposed = transform(
                resource, steps=[steps.table_normalize(), steps.table_transpose()]
            )

            package = transform(
                package,
                steps=[
                    steps.resource_remove(name=args["name"]),
                    steps.resource_add(transposed),
                ],
            )
        elif command == "table_pivot":
            # Get all columns in the pivoted table, building the
            # arguments for the `table_pivot` step
            columns = {
                f"f{idx+1}": column for idx, column in enumerate(args["columns"])
            }

            resource = package.get_resource(args["name"])
            pivoted = transform(
                resource,
                steps=[
                    steps.table_normalize(),
                    steps.table_pivot(aggfun=sum, **columns),
                ],
            )

            # TODO: move to a single "replace"
            package = transform(
                package,
                steps=[
                    steps.resource_remove(name=args["name"]),
                    steps.resource_add(pivoted),
                ],
            )

        else:
            # Fallback
            raise ValueError(f"Unknown command: {command}")

    return package


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
