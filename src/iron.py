"""
Provide the iron algorithm for authentication.
"""
import base64
import json
from json import JSONDecodeError
from typing import (
    Any,
    Dict,
    Optional,
)

from Crypto.Cipher import AES
from Crypto.Hash import SHA1
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import random

from constants import (
    ALGORITHMS,
    ENCRYPTION_DEFAULT_OPTIONS,
    MAC_PREFIX,
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

        Raises:
            ConfigurationError: when the algorithm is not correctly configured in the options.

        Returns:
            The algorithm name, as a string.
        """
        try:
            return self.options['algorithm']
        except KeyError:
            raise ConfigurationError(message='Bad options: `algorithm` is missing')

    @property
    def algorithm_mode(self) -> str:
        """
        Get the algorithm mode of the current iron instance.

        Raises:
            ConfigurationError: when the algorithm mode is not correctly configured in the options.

        Returns:
            The algorithm mode, as a string.
        """
        try:
            return self.options['algorithm_mode']
        except KeyError:
            raise ConfigurationError(message='Bad options: `algorithm_mode` is missing')

    @property
    def min_password_length(self) -> int:
        """
        Get the minimum password length of the current iron instance.

        Raises:
            ConfigurationError: when the minimum password length is not correctly configured in the options.

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

    @salt.setter
    def salt(self, value: str) -> None:
        """
        Set the salt of the current iron instance.

c
        """
        self.options['salt'] = value

    @property
    def salt_bits(self) -> Optional[int]:
        """
        Get the salt bits of the current iron instance.

        Returns:
            The salt bits, as an integer. If not set, then returns `None`.
        """
        return self.options.get('salt_bits')

    @property
    def initialization_vector(self) -> Optional[str]:
        """
        Get the initialization vector of the current iron instance.

        Returns:
            The initialization vector, as a string. If not set, then returns `None`.
        """
        return self.options.get('initialization_vector')

    @initialization_vector.setter
    def initialization_vector(self, value: str) -> None:
        """
        Set the initialization vector of the current iron instance.

        Arguments:
            value (str) : new value for the initialization vector property.
        """
        self.options['initialization_vector'] = value

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
        if self.initialization_vector:
            encryption_key.initialization_vector = self.initialization_vector
        elif algorithm.get('initialization_vector_bits'):
            encryption_key.initialization_vector = random.getrandbits(k=algorithm['initialization_vector_bits'])

        return encryption_key

    def decrypt(self, data: str) -> bytes:
        """
        Decrypt data.

        Arguments:
            data (str): encrypted data.

        Returns:
            The data in a decrypted format, as bytes.
        """
        key = self._generate_key()

        decipher = AES.new(mode=self.algorithm_mode, key=key.key, iv=key.initialization_vector)
        deciphered_data = decipher.decrypt(data)

        return deciphered_data

    def unseal(self, sealed: str) -> Dict[str, Any]:
        """
        Decrypt and validate a sealed string.

        Arguments:
            sealed (str): sealed string to be derypted.

        Raises:
            ValueError: when the sealed string is incorrect or is not a valid JSON.

        Returns:
            The unsealed information, as a dictionary.
        """
        parts = sealed.split('*')
        try:
            mac_prefix, password_id, encryption_salt, encryption_iv, encrypted_b64, expiration, hmac_salt, hmac = parts
        except ValueError:
            raise ValueError('Incorrect number of sealed omponents in the provided encrypted string')

        if mac_prefix != MAC_PREFIX:
            raise ValueError('Wrong mac prefix in the provided encrypted string')

        encrypted_value = base64.urlsafe_b64decode(encrypted_b64)

        self.salt = encryption_salt

        try:
            padded_encryption_initialization_vector = encryption_iv + '=' * (-len(encryption_iv) % 4)
            self.initialization_vector = base64.urlsafe_b64decode(padded_encryption_initialization_vector)
        except Exception as error:
            raise error

        decrypted_value = self.decrypt(data=encrypted_value)

        decrypted_value_without_padding = decrypted_value.replace(b'\x0f', b'')
        try:
            return json.loads(decrypted_value_without_padding)
        except (UnicodeDecodeError, JSONDecodeError):
            print('Failed parsing sealed object JSON')
            return {}
