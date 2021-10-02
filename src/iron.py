"""
Provide the Iron algorithm for authentication.
"""
from typing import (
    Any,
    Dict,
    Optional,
)

from Crypto.Hash import SHA1
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import random

from constants import (
    ALGORITHMS,
    ENCRYPTION_DEFAULT_OPTIONS,
    EncryptionKey,
)
from errors import ConfigurationError


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

        Raises:
            ConfigurationError: when the encryption password or settings are not correctly configured.
        """
        if not password:
            raise ConfigurationError(message='Empty password')

        if not options or not isinstance(options, dict):
            raise ConfigurationError(message='Bad options')

        self.password = password
        self.options = options if options else ENCRYPTION_DEFAULT_OPTIONS

    @property
    def algorithm(self) -> str:
        """
        Get the algorithm of the current iron instance.

        Returns:
            The algorithm name, as a string.
        """
        try:
            return self.options['algorithm']
        except KeyError:
            raise ConfigurationError(message='Bad options: `algorithm` is missing')

    @property
    def min_password_length(self) -> int:
        """
        Get the minimum password length of the current iron instance.

        Returns:
            The minimum password length, as an integer.
        """
        try:
            return self.options['min_password_length']
        except KeyError:
            raise ConfigurationError(message='Bad options: `min_password_length` is missing')

    @property
    def salt(self) -> Optional[str]:
        """
        Get the salt of the current iron instance.

        Returns:
            The salt, as a string. If not set, then returns `None`.
        """
        return self.options.get('salt')

    @property
    def salt_bits(self) -> Optional[int]:
        """
        Get the salt bits of the current iron instance.

        Returns:
            The salt bits, as an integer. If not set, then returns `None`.
        """
        return self.options.get('salt_bits')

    def _generate_key(self) -> EncryptionKey:
        """
        Generate a unique encryption key, considering that the password is not a node.js Buffer instance.

        Raises:
            ConfigurationError: when the encryption password or settings are not correctly configured.

        Returns:
            A unique encryption key, as an `EncryptionKey` with salt and initialization vector (IV).
        """
        try:
            algorithm = ALGORITHMS[self.algorithm]
        except KeyError:
            raise ConfigurationError(f'Unknown algorithm: {self.algorithm}')

        if len(self.password) < self.min_password_length:
            raise ConfigurationError(f'Password string too short (min {self.min_password_length} characters required)')

        if not self.salt:
            if not self.salt_bits:
                raise ConfigurationError('Missing both salt and salt_bits options')

            random_salt = random.getrandbits(k=self.salt_bits)
            salt = str(random_salt)

        derived_key = PBKDF2(
            password=self.password,
            salt=salt,
            dkLen=int(algorithm['key_bits'] / 8),
            count=self.options['iterations'],
            hmac_hash_module=SHA1,
        )

        encryption_key = EncryptionKey(
            key=derived_key,
            salt=salt,
        )
        if self.options.get('iv'):
            encryption_key.initialization_vector = self.options['iv']
        elif algorithm.get('iv_bits'):
            encryption_key.initialization_vector = random.getrandbits(k=algorithm['iv_bits'])

        return encryption_key
