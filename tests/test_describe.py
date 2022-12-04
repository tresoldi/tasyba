"""
test_describe
=============

Tests for automatic description of resources and packages in
interface with frictionless.
"""

# Import Python standard libraries
from pathlib import Path

# Import 3rd-party libraries
import yaml

# Import the library
import tasyba

# Obtain the path to the test data
TEST_DATA_PATH = Path(__file__).parent / "data"


def test_describe_resource():
    """Test automatic description of a resource."""

    # Obtain the resource metadata, serialize it, and compare it to the
    # expected output loaded directly from a YAML file. Note that we
    # don't compare the paths, as they are absolute and will differ
    # between machines.
    resource_path = TEST_DATA_PATH / "countries.csv"
    resource = tasyba.describe_resource(resource_path)
    resource.pop("path")

    expected = yaml.safe_load((TEST_DATA_PATH / "countries.yaml").read_text())
    expected.pop("path")

    # Compare the two dictionaries
    assert resource == expected
