import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import threading

from core.encryptor import encrypt_file
from core.decryptor import decrypt_file


class SecureFileVaultGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Moksh's Secure File Vault")
        self.root.geometry("520x520")
        self.root.resizable(False, False)

        self.file_path = None
        self.last_password = None  # 🔐 store encryption password

        tk.Label(root, text="🔐 Secure File Vault", font=("Arial", 18, "bold")).pack(pady=10)

        self.file_label = tk.Label(
            root,
            text="Select a file to encrypt or decrypt",
            relief="groove",
            height=3,
            width=55
        )
        self.file_label.pack(pady=10)

        tk.Button(root, text="Select File", command=self.select_file).pack()

        self.file_info = tk.Label(root, text="No file selected")
        self.file_info.pack(pady=5)

        tk.Label(root, text="Password").pack()
        self.password = tk.Entry(root, show="*", width=30)
        self.password.pack()

        self.strength = ttk.Progressbar(root, length=200)
        self.strength.pack(pady=5)
        self.password.bind("<KeyRelease>", self.check_strength)

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Encrypt", width=12, command=self.encrypt).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="Decrypt", width=12, command=self.decrypt).grid(row=0, column=1, padx=10)

        self.progress = ttk.Progressbar(root, length=300)
        self.progress.pack(pady=10)

        self.logs = tk.Text(root, height=8, width=60)
        self.logs.pack()

    # ---------- Safe UI helpers ----------

    def ui(self, fn):
        self.root.after(0, fn)

    def log(self, msg):
        self.ui(lambda: (
            self.logs.insert(tk.END, f"[+] {msg}\n"),
            self.logs.see(tk.END)
        ))

    # ---------- Actions ----------

    def select_file(self):
        self.file_path = filedialog.askopenfilename()
        if self.file_path:
            size = os.path.getsize(self.file_path)
            self.file_info.config(
                text=f"{os.path.basename(self.file_path)} | {size} bytes"
            )
            self.log("File selected")

    def check_strength(self, event=None):
        score = min(len(self.password.get()) * 10, 100)
        self.strength["value"] = score

    def encrypt(self):
        if not self.file_path:
            messagebox.showerror("Error", "Select a file first")
            return

        pwd = self.password.get().strip()
        if not pwd:
            messagebox.showerror("Error", "Password required")
            return

        self.last_password = pwd  # 🔐 lock password
        self.start_task("encrypt")

    def decrypt(self):
        if not self.file_path or not self.file_path.endswith(".secfile"):
            messagebox.showerror("Invalid file", "Please select a .secfile")
            return

        if not self.last_password:
            messagebox.showerror(
                "Error",
                "Password was cleared.\nPlease re-encrypt or restart the app."
            )
            return

        self.start_task("decrypt")

    def start_task(self, mode):
        self.ui(lambda: self.progress.config(value=0))
        threading.Thread(target=self.process, args=(mode,), daemon=True).start()

    # ---------- Core logic ----------

    def process(self, mode):
        try:
            self.ui(lambda: self.progress.config(value=20))
            self.log(f"{mode.capitalize()} started")

            if mode == "encrypt":
                encrypt_file(self.file_path, self.last_password)

                encrypted = self.file_path + ".secfile"
                self.file_path = encrypted

                self.ui(lambda: self.file_info.config(
                    text=f"{os.path.basename(encrypted)} | encrypted"
                ))

                self.log("Encryption successful")
                self.log("Original file securely deleted")
                self.log("Password locked for decryption")

            else:
                decrypt_file(self.file_path, self.last_password)
                self.log("Decryption successful")
                self.log("Original filename restored")

                self.file_path = None
                self.last_password = None
                self.ui(lambda: self.file_info.config(text="No file selected"))

            self.ui(lambda: self.progress.config(value=100))

        except Exception as e:
            msg = str(e)
            self.log(f"Error: {msg}")
            self.ui(lambda m=msg: messagebox.showerror("Security Error", m))


if __name__ == "__main__":
    root = tk.Tk()
    SecureFileVaultGUI(root)
    root.mainloop()
