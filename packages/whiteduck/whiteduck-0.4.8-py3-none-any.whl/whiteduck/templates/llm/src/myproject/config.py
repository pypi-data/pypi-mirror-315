"""Configuration handling for the project."""

from typing import Any

from decouple import config as decouple_config


def config(key: str, default: Any = None, cast: type = str) -> Any | None:
    """Get configuration value, treating empty strings and 'None' as None.

    Args:
        key: The configuration key to look up
        default: The default value if key is not found
        cast: The type to cast the value to

    Returns:
        The configuration value, or None if the value is an empty string or 'None'
    """
    value = decouple_config(key, default=default, cast=cast)
    if value == "" or value == "None":
        return None
    return value
