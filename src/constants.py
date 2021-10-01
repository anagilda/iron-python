"""
Provide constants for encryption and decryption with iron.
"""
from Crypto.Cipher import AES

ENCRYPTION_DEFAULT_OPTIONS = {
    'salt_bits': 256,
    'algorithm': 'aes-256-cbc',
    'algorithm_mode': AES.MODE_CBC,
    'iterations': 1,
    'min_password_length': 32,
}
