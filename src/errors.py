"""
Provide errors for encryption and decryption with iron.
"""
from typing import Optional


class ConfigurationError(Exception):
    """
    Configuration error implementation.

    It's raised when some configuration value is not valid or missing.
    """

    default_message = 'Some configurations are incorrect or missing. Please check them'

    def __init__(self, message: Optional[str] = None) -> None:
        """
        Construct the object.

        Arguments:
            message (str): custom detailed error message.
        """
        super().__init__(message or self.default_message)
