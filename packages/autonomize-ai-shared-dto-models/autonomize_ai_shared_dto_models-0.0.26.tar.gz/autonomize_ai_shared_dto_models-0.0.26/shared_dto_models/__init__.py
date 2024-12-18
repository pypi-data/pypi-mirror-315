import logging
import toml
from pydantic import BaseModel, ValidationError
from typing import Optional

class PackageStatusDto(BaseModel):
    package_name: str
    version: str
    decorators_working: bool
    description: Optional[str] = None

# Function to read values from pyproject.toml
def get_pyproject_data() -> dict:
    try:
        # Load the pyproject.toml file
        pyproject_data = toml.load("pyproject.toml")
        # Extract relevant data
        package_data = pyproject_data.get("tool", {}).get("poetry", {})
        return {
            "package_name": package_data.get("name", "Unknown Package"),
            "version": package_data.get("version", "0.0.1"),
            "description": package_data.get("description", "No description provided")
        }
    except Exception as e:
        logging.warning(f"Failed to read pyproject.toml: {e}")
        # Return default values in case of an error
        return {
            "package_name": "Unknown Package",
            "version": "0.0.1",
            "description": "No description provided"
        }

# Function to get package details and validate it
def get_package_details() -> PackageStatusDto:
    try:
        # Get the data from pyproject.toml
        INITIAL_DATA = get_pyproject_data()

        # Create an instance of PackageStatusDto using the initial data
        package_details = PackageStatusDto(**INITIAL_DATA)

        # You can add additional validation if needed
        return package_details
    except ValidationError as e:
        logging.warning(f"Package initialization check failed: {e}")
        # Return the initial data with decorators_working set to False if validation fails
        INITIAL_DATA = get_pyproject_data()
        return PackageStatusDto(**{**INITIAL_DATA, "decorators_working": False})

# Define the DTO (Data Transfer Object) class similar to PackageStatusDto
__all__ = ["PackageStatusDto", "get_pyproject_data", "get_package_details"]