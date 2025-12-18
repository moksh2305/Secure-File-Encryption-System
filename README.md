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

<img width="516" height="545" alt="gui 1" src="https://github.com/user-attachments/assets/45228615-229f-411b-b33a-29f8170f6c48" />


<img width="516" height="547" alt="gui successful encryption" src="https://github.com/user-attachments/assets/b4977db7-4303-4723-ab5c-53788398cb52" />


<img width="839" height="544" alt="gui password error" src="https://github.com/user-attachments/assets/55e4c15e-98b0-40c3-ba57-798201bb5bf7" />


<img width="514" height="545" alt="gui successful decryption" src="https://github.com/user-attachments/assets/475a202e-1074-4161-a8ff-a2aa74901b42" />


<img width="510" height="637" alt="web" src="https://github.com/user-attachments/assets/925b13f2-b29e-40d5-a9e1-a33198feceb3" />


<img width="865" height="634" alt="web select file" src="https://github.com/user-attachments/assets/1848b522-f016-48b1-a2a7-d99f5f7d3b3b" />


<img width="377" height="275" alt="web enter password" src="https://github.com/user-attachments/assets/947ce559-1e70-40fd-b752-73341dd953f7" />


<img width="374" height="361" alt="web select sec file " src="https://github.com/user-attachments/assets/4dba7efb-9b52-4ace-ac84-ee74400fcc34" />


<img width="1366" height="643" alt="web decryption successful" src="https://github.com/user-attachments/assets/2d09e160-77d7-439e-99ae-7379e10796c0" />



📄 License

This project is for _educational and demonstration_ purposes.

👤 Author

**Moksh Shah**

Cybersecurity & Software Engineering Project
