import struct
import json

MAGIC = b"SECFILE"
VERSION = 2   # ⬅ bumped version


def pack(salt, iv, enc_aes_key, hmac, ciphertext, metadata: dict):
    meta_bytes = json.dumps(metadata).encode()

    return (
        MAGIC +
        struct.pack("B", VERSION) +
        struct.pack("H", len(salt)) + salt +
        struct.pack("H", len(iv)) + iv +
        struct.pack("H", len(enc_aes_key)) + enc_aes_key +
        struct.pack("H", len(hmac)) + hmac +
        struct.pack("I", len(meta_bytes)) + meta_bytes +
        ciphertext
    )


def unpack(blob):
    offset = 0

    if blob[:7] != MAGIC:
        raise ValueError("Invalid file format")

    offset += 7
    version = blob[offset]
    offset += 1

    def read_chunk(fmt):
        nonlocal offset
        size = struct.calcsize(fmt)
        val = struct.unpack(fmt, blob[offset:offset+size])[0]
        offset += size
        return val

    def read_bytes():
        nonlocal offset
        length = read_chunk("H")
        data = blob[offset:offset+length]
        offset += length
        return data

    salt = read_bytes()
    iv = read_bytes()
    enc_aes_key = read_bytes()
    mac = read_bytes()

    meta_len = read_chunk("I")
    metadata = json.loads(blob[offset:offset+meta_len].decode())
    offset += meta_len

    ciphertext = blob[offset:]

    return salt, iv, enc_aes_key, mac, metadata, ciphertext
