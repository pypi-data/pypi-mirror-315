from io import StringIO

from django.core.exceptions import ValidationError
from dotenv import dotenv_values

# TODO: dotenv kinda sucks - consider alternatives like `environs`
# consider https://docs.pydantic.dev/latest/concepts/pydantic_settings/#settings-management


def parse_env_contents(contents: str) -> dict:
    """Checks that the string is in valid "dotenv" format"""
    try:
        # Parse the .env content from a string
        env_data = dotenv_values(stream=StringIO(contents))
    except Exception as e:  # It's a good idea to catch more specific exceptions
        raise ValidationError(f"Invalid Environment Variables: {e}")
    for key, value in env_data.items():
        if value is None or value == "":
            raise ValidationError(
                f"Invalid dotenv format: '{key}' lacks a non-empty value."
            )
        if " " in key:
            raise ValidationError(f"Invalid dotenv format: '{key}' contains a space.")
        if "=" in key:
            raise ValidationError(
                f"Invalid dotenv format: '{key}' contains an equal sign."
            )
    return env_data
