from cryptography.hazmat.primitives import hmac, hashes


def generate_hmac(key: bytes, data: bytes) -> bytes:
    h = hmac.HMAC(key, hashes.SHA256())
    h.update(data)
    return h.finalize()


def verify_hmac(key: bytes, data: bytes, mac: bytes):
    h = hmac.HMAC(key, hashes.SHA256())
    h.update(data)
    h.verify(mac)

