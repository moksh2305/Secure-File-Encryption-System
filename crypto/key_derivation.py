import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend


def derive_key(password: str, salt: bytes = None) -> tuple[bytes, bytes]:
    """
    Derives a 256-bit key from a password using PBKDF2-HMAC-SHA256.
    Returns (key, salt)
    """
    if salt is None:
        salt = os.urandom(16)  # 128-bit salt

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,              # 256-bit key
        salt=salt,
        iterations=100_000,     # Industry standard
        backend=default_backend()
    )

    key = kdf.derive(password.encode())
    return key, salt

if __name__ == "__main__":
    password = "StrongPassword@123"

    key1, salt1 = derive_key(password)
    key2, _ = derive_key(password, salt1)

    print("Key 1:", key1.hex())
    print("Key 2:", key2.hex())
    print("Keys match:", key1 == key2)
