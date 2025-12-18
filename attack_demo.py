import shutil
from core.decryptor import decrypt_file

print("\n=== ATTACK DEMO ===\n")

print("[1] Wrong password attack")
try:
    decrypt_file("test.txt.secfile", "wrongpassword")
except Exception as e:
    print("✔ Attack blocked:", e)

print("\n[2] Tampering attack")
shutil.copy("test.txt.secfile", "tampered.secfile")

with open("tampered.secfile", "r+b") as f:
    f.seek(50)
    f.write(b"\x00")

try:
    decrypt_file("tampered.secfile", "mypassword123")
except Exception as e:
    print("✔ Tampering detected:", e)

print("\n[3] Legitimate access")
decrypt_file("test.txt.secfile", "mypassword123")
print("✔ Legitimate decryption successful")
