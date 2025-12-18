const fileInput = document.getElementById("fileInput");
const dropZone = document.getElementById("dropZone");
const fileInfo = document.getElementById("fileInfo");
const password = document.getElementById("password");
const strengthBar = document.getElementById("strength");
const strengthText = document.getElementById("strengthText");
const progress = document.getElementById("progress");
const statusText = document.getElementById("status");

let selectedFile = null;

/* Drag & Drop */
dropZone.onclick = () => fileInput.click();
dropZone.ondragover = e => { e.preventDefault(); dropZone.style.background="#334155"; };
dropZone.ondragleave = () => dropZone.style.background="";
dropZone.ondrop = e => {
    e.preventDefault();
    selectedFile = e.dataTransfer.files[0];
    showFileInfo();
};

fileInput.onchange = () => {
    selectedFile = fileInput.files[0];
    showFileInfo();
};

function showFileInfo() {
    if (!selectedFile) return;
    fileInfo.innerText = `${selectedFile.name} | ${selectedFile.size} bytes`;
}

/* Password strength */
password.oninput = () => {
    let score = Math.min(password.value.length * 10, 100);
    strengthBar.value = score;
    strengthText.innerText =
        score < 40 ? "Weak" : score < 70 ? "Medium" : "Strong";
};

/* Show/Hide password */
document.getElementById("togglePwd").onclick = () => {
    password.type = password.type === "password" ? "text" : "password";
};

/* Crypto helpers */
async function deriveKey(pwd, salt) {
    const enc = new TextEncoder();
    const baseKey = await crypto.subtle.importKey(
        "raw", enc.encode(pwd), "PBKDF2", false, ["deriveKey"]
    );
    return crypto.subtle.deriveKey(
        { name: "PBKDF2", salt, iterations: 100000, hash: "SHA-256" },
        baseKey,
        { name: "AES-GCM", length: 256 },
        false,
        ["encrypt", "decrypt"]
    );
}

/* Encrypt */
async function encryptFile() {
    if (!selectedFile || !password.value) {
        alert("File and password required");
        return;
    }

    statusText.innerText = "Encrypting...";
    progress.value = 20;

    const data = await selectedFile.arrayBuffer();
    const salt = crypto.getRandomValues(new Uint8Array(16));
    const iv = crypto.getRandomValues(new Uint8Array(12));
    const key = await deriveKey(password.value, salt);

    const encrypted = await crypto.subtle.encrypt(
        { name: "AES-GCM", iv }, key, data
    );

    progress.value = 80;

    const meta = new TextEncoder().encode(JSON.stringify({
        filename: selectedFile.name
    }));

    const blob = new Blob([salt, iv, meta, new Uint8Array(encrypted)]);
    download(blob, selectedFile.name + ".secfile");

    progress.value = 100;
    statusText.innerText = "Encryption complete ✔";
}

/* Decrypt */
async function decryptFile() {
    if (!selectedFile || !password.value) {
        alert("File and password required");
        return;
    }

    statusText.innerText = "Decrypting...";
    progress.value = 20;

    const buffer = await selectedFile.arrayBuffer();
    const data = new Uint8Array(buffer);

    const salt = data.slice(0,16);
    const iv = data.slice(16,28);
    const metaEnd = data.indexOf(125, 28) + 1; // '}'
    const meta = JSON.parse(new TextDecoder().decode(data.slice(28, metaEnd)));
    const ciphertext = data.slice(metaEnd);

    try {
        const key = await deriveKey(password.value, salt);
        const decrypted = await crypto.subtle.decrypt(
            { name: "AES-GCM", iv }, key, ciphertext
        );

        progress.value = 100;
        statusText.innerText = "Decryption complete ✔";
        download(new Blob([decrypted]), meta.filename);

    } catch {
        alert("❌ Decryption failed\nPossible reasons:\n• Wrong password\n• File modified");
        statusText.innerText = "Decryption failed ❌";
    }
}

function download(blob, filename) {
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = filename;
    a.click();
}
