# config tools

import os


def parse_bool(env_var: str, default: bool) -> bool:
    """
    Parse a boolean value from an environment variable.

    If the environment variable is not set, return the default value.
    If the environment variable is set, it must be one of the following:
    - "true", "1", "yes" (case-insensitive) for True
    - "false", "0", "no" (case-insensitive) for False
    """
    value = os.getenv(env_var)
    if value is None:
        return default
    if value.lower() in ["true", "1", "yes"]:
        return True
    if value.lower() in ["false", "0", "no"]:
        return False
    raise ValueError(f"Invalid boolean value for {env_var=}: {value=}")
    
