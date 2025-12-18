import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


class AESUtil:
    @staticmethod
    def encrypt(data: bytes, key: bytes) -> tuple[bytes, bytes]:
        """
        Encrypts data using AES-256-GCM.
        Returns (ciphertext, iv)
        """
        if len(key) != 32:
            raise ValueError("AES key must be 256 bits")

        iv = os.urandom(12)  # 96-bit nonce
        aesgcm = AESGCM(key)
        ciphertext = aesgcm.encrypt(iv, data, None)

        return ciphertext, iv

    @staticmethod
    def decrypt(ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
        """
        Decrypts AES-256-GCM encrypted data.
        Raises exception if tampered.
        """
        aesgcm = AESGCM(key)
        return aesgcm.decrypt(iv, ciphertext, None)