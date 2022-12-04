"""
Module with functions for interfacing with the frictionless framework.
"""

# Import Python standard libraries
from pathlib import Path
from typing import *

# Import 3rd-party libraries
import frictionless

# TODO: implement a fallback with our own implementation, with
#       extremely simple descriptions (mostly the list of columns)
#       but able to handle most files.
def describe_resource(
    filename: Union[Path, str], validate=True
) -> frictionless.Resource:
    """
    Obtain the frictionless description of a resource (i.e., single table).

    Note that the function will by default also perform pre-resource
    validation, which can be disabled by setting the `validate` parameter.
    The validation will stop execution and show the error report if the
    resource is not valid.

    Parameters
    ----------
    filename : Union[Path,str]
        The path to the resource to describe.
    validate : bool, optional
        Whether to perform pre-resource validation, by default True.
    """

    if validate:
        # Validate the resource
        report = frictionless.validate(filename)
        if not report["valid"]:
            print(report.to_summary())  # TODO: to logging
            raise ValueError(
                "Resource is not valid, please see validation report above."
            )

    resource = frictionless.describe(filename)

    return resource
