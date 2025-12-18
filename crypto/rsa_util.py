import os
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

KEYSTORE_DIR = "keystore"
PRIVATE_KEY_PATH = os.path.join(KEYSTORE_DIR, "private_key.pem")
PUBLIC_KEY_PATH = os.path.join(KEYSTORE_DIR, "public_key.pem")

# 🔐 Fixed internal keystore password
KEYSTORE_PASSWORD = b"SECUREFILEVAULT_INTERNAL_KEY"


def ensure_keystore():
    os.makedirs(KEYSTORE_DIR, exist_ok=True)


def generate_and_store_keys():
    ensure_keystore()

    if os.path.exists(PRIVATE_KEY_PATH):
        return  # already exists

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()

    with open(PRIVATE_KEY_PATH, "wb") as f:
        f.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.BestAvailableEncryption(
                    KEYSTORE_PASSWORD
                )
            )
        )

    with open(PUBLIC_KEY_PATH, "wb") as f:
        f.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )


def load_public_key():
    with open(PUBLIC_KEY_PATH, "rb") as f:
        return serialization.load_pem_public_key(f.read())


def load_private_key():
    with open(PRIVATE_KEY_PATH, "rb") as f:
        return serialization.load_pem_private_key(
            f.read(),
            password=KEYSTORE_PASSWORD
        )


def encrypt_key(aes_key, public_key):
    return public_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )


def decrypt_key(enc_key, private_key):
    return private_key.decrypt(
        enc_key,
        padding.OAEP(
            mgf=padding.MGF1(hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
