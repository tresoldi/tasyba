"""
Module with functions for interfacing with the frictionless framework.
"""

# Import Python standard libraries
from pathlib import Path
from typing import *
import logging

# Import 3rd-party libraries
import frictionless


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
            logging.error(report.to_summary())
            raise ValueError(
                "Resource is not valid, please see validation report above."
            )

    resource = frictionless.describe(filename)

    return resource
