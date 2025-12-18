import sys
from core.encryptor import encrypt_file
from core.decryptor import decrypt_file


if len(sys.argv) < 4:
    print("Usage:")
    print("Encrypt: python main_cli.py encrypt <file> <password>")
    print("Decrypt: python main_cli.py decrypt <file.secfile> <password>")
    sys.exit(1)

mode, file, password = sys.argv[1:]

if mode == "encrypt":
    encrypt_file(file, password)
    print("File encrypted successfully")

elif mode == "decrypt":
    decrypt_file(file, password)
    print("File decrypted successfully")

else:
    print("Invalid mode")
