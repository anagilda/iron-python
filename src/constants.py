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


ALGORITHMS = {
    'aes-128-ctr': {'key_bits': 128, 'initialization_vector_bits': 128},
    'aes-256-cbc': {'key_bits': 256, 'initialization_vector_bits': 128},
    'sha256': {'key_bits': 256},
}

ENCRYPTION_DEFAULT_OPTIONS = {
    'salt_bits': 256,
    'algorithm': 'aes-256-cbc',
    'algorithm_mode': AES.MODE_CBC,
    'iterations': 1,
    'min_password_length': 32,
}

MAC_FORMAT_VERSION = '2'
MAC_PREFIX = 'Fe26.' + MAC_FORMAT_VERSION
