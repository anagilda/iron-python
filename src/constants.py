"""
Provide constants for encryption and decryption with iron.
"""
from dataclasses import dataclass

from Crypto.Cipher import AES


@dataclass
class EncryptionKey:
    """
    Encryption key implementation.
    """

    key: bytes = b''
    salt: str = ''
    initialization_vector: bytes = b''


ENCRYPTION_DEFAULT_OPTIONS = {
    'salt_bits': 256,
    'algorithm': 'aes-256-cbc',
    'algorithm_mode': AES.MODE_CBC,
    'iterations': 1,
    'min_password_length': 32,
}
