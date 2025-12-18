import os

from crypto.key_derivation import derive_key
from crypto.key_split import split_keys
from crypto.aes_util import AESUtil
from crypto.rsa_util import generate_and_store_keys, load_public_key, encrypt_key
from crypto.hmac_util import generate_hmac
from crypto.secure_delete import secure_delete
from core.file_package import pack


def encrypt_file(filepath, password):
    # Read plaintext file
    with open(filepath, "rb") as f:
        data = f.read()

    # Derive master key from password
    master_key, salt = derive_key(password)

    # 🔐 Proper key separation
    aes_key, hmac_key = split_keys(master_key)

    # Encrypt file data
    ciphertext, iv = AESUtil.encrypt(data, aes_key)

    # 🔑 Ensure persistent RSA keys exist
    generate_and_store_keys()
    
    # Load public key for AES key wrapping
    public_key = load_public_key()
    enc_aes_key = encrypt_key(aes_key, public_key)

    # 🔎 Integrity protection
    mac = generate_hmac(hmac_key, ciphertext)

    # 🔐 METADATA (encrypted inside container)
    metadata = {
        "filename": os.path.basename(filepath),
        "size": len(data)
    }

    # Package everything into secure container
    package = pack(
        salt=salt,
        iv=iv,
        enc_aes_key=enc_aes_key,
        hmac=mac,
        ciphertext=ciphertext,
        metadata=metadata
    )

    # Write encrypted file
    out_file = filepath + ".secfile"
    with open(out_file, "wb") as f:
        f.write(package)

    # 🧨 Securely delete original plaintext file
    secure_delete(filepath)
