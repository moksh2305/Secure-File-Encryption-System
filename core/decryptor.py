from crypto.key_derivation import derive_key
from crypto.key_split import split_keys
from crypto.aes_util import AESUtil
from crypto.rsa_util import load_private_key, decrypt_key
from crypto.hmac_util import verify_hmac
from core.file_package import unpack


def decrypt_file(secfile: str, password: str):
    """
    Decrypts a .secfile using the provided password.
    Restores original filename from encrypted metadata.
    """

    # Read encrypted file
    with open(secfile, "rb") as f:
        blob = f.read()

    # Unpack secure container (VERSION 2)
    salt, iv, enc_aes_key, mac, metadata, ciphertext = unpack(blob)

    # Re-derive master key from password
    master_key, _ = derive_key(password, salt)

    # 🔐 Proper key separation
    aes_key, hmac_key = split_keys(master_key)

    # 🔎 Verify integrity FIRST (fail-fast)
    verify_hmac(hmac_key, ciphertext, mac)

    # 🔑 Load persistent private RSA key from keystore
    private_key = load_private_key()

    # 🔓 Decrypt AES key using RSA
    aes_key = decrypt_key(enc_aes_key, private_key)

    # 🔓 Decrypt file contents
    data = AESUtil.decrypt(ciphertext, aes_key, iv)

    # 🔁 Restore original filename
    output_name = metadata.get("filename", "decrypted_output")

    with open(output_name, "wb") as f:
        f.write(data)

    return output_name
