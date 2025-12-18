from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes


def split_keys(master_key: bytes) -> tuple[bytes, bytes]:
    """
    Derives independent AES and HMAC keys from master key
    """
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=64,   # 32 AES + 32 HMAC
        salt=None,
        info=b"SecureFileVault key separation"
    )

    derived = hkdf.derive(master_key)
    return derived[:32], derived[32:]
