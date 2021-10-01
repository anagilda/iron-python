"""
Provide the Iron algorithm for authentication.
"""
from typing import (
    Any,
    Dict,
    Optional,
)

from constants import ENCRYPTION_DEFAULT_OPTIONS


class Iron:
    """
    Iron algorithm implementation.

    References:
    - https://github.com/hapijs/iron
    """

    def __init__(self, password: str, options: Optional[Dict[str, Any]] = None) -> None:
        """
        Construct the object.

        Arguments:
            password (str): encryption password.
            options (dict): encryption options.
        """
        self.password = password
        self.options = options if options else ENCRYPTION_DEFAULT_OPTIONS