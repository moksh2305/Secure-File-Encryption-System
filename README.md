**🔐 Secure File Vault**

Secure File Vault is a multi-interface cybersecurity project that provides strong file encryption, integrity protection, and secure deletion, implemented using industry-standard cryptographic practices.
The project is designed to demonstrate real-world security engineering, not just academic encryption.

It includes:

A CLI tool
A Desktop GUI (Tkinter)
A Zero-knowledge Web UI (client-side encryption)

**🚀 Key Features**

_🔒 Cryptography_

1. AES-256 symmetric encryption for file confidentiality
2. HMAC-SHA256 for integrity verification (tamper detection)
3. PBKDF2 for secure password-based key derivation
4. RSA-2048 for secure AES key wrapping
5. Proper key separation (encryption key ≠ integrity key)

_🛡️ Security Engineering_

1. Fail-fast integrity checks (decrypt only after verification)
2. Encrypted metadata (original filename, size)
3. Secure file deletion (multi-pass overwrite + removal)
4. Persistent keystore with safe key lifecycle handling
5. Protection against tampering and wrong-password attacks

**🖥️ Interfaces**

**1️⃣ Command Line Interface (CLI)**

‣ Encrypt and decrypt files via terminal

‣ Suitable for scripting and technical validation

Run:
python -m ui.main_cli encrypt file.txt password

python -m ui.main_cli decrypt file.txt.secfile password


**2️⃣ Desktop GUI (Tkinter)**

‣ File picker with encryption & decryption

‣ Password strength indicator

‣ Progress bar and security logs

‣ Automatic handling of encrypted files

‣ User-friendly error messages

Run:
python -m ui.gui_app


**3️⃣ Web Interface (Zero-Knowledge)**

‣ Client-side encryption using Web Crypto API

‣ Drag-and-drop file support

‣ Password strength meter

‣ AES-256-GCM encryption in browser

‣ No file, password, or key ever leaves the browser

Open:
web/index.html

or Run:
python -m http.server

**Threats & Mitigations**

<img width="367" height="180" alt="image" src="https://github.com/user-attachments/assets/265438c2-6c71-43d6-a672-26b49cd85557" />

**NOTE: The keystore/ directory is not committed to GitHub for security reasons.**

**🧪 Security Behavior (Expected)**

✔ Correct password → successful decryption
❌ Wrong password → integrity failure
❌ Modified encrypted file → decryption blocked
✔ Original filename restored on decryption

These behaviors are intentional and required for secure systems

**🏆 What This Project Demonstrates**

● Real-world cryptographic design
● Secure key lifecycle management
● UI + security interaction handling
● Zero-knowledge encryption principles
● Defensive programming practices


📄 License
This project is for _educational and demonstration_ purposes.

👤 Author
**Moksh Shah**
Cybersecurity & Software Engineering Project
