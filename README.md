Local Secure Password Manager

A lightweight, terminal-based password manager built in Python. This tool stores your credentials locally using industry-standard authenticated encryption, ensuring your data remains private and secure on your own machine.

It features a "Zero-Knowledge" architecture where your Master Password is never stored or written to disk.
🔐 Security Architecture

This project does not roll its own crypto. It relies on the reputable cryptography library and implements standard, robust primitives:

    Encryption: AES-GCM (Galois/Counter Mode). This provides both confidentiality (encryption) and integrity (authentication), ensuring that data cannot be tampered with without detection.

    Key Derivation: PBKDF2-HMAC-SHA256 with 1,200,000 iterations. This high iteration count makes brute-force attacks computationally expensive for attackers.

    Per-Entry Salting: Every single password entry is encrypted with a unique, randomly generated 16-byte salt and a 12-byte nonce. This prevents rainbow table attacks and ensures that identical passwords result in completely different encrypted data.

    Secure Randomness: All secrets and passwords are generated using Python's secrets module (CSPRNG), not the standard random library.

🚀 Features

    Local Storage: All data is stored in a local SQLite database (passwords.db).

    Clipboard Integration: Automatically copies retrieved passwords to your clipboard for easy pasting.

    Password Generator: Built-in tool to generate strong, random passwords using secrets.

    Hidden Inputs: Uses getpass to ensure passwords are not displayed on screen while typing.

🛠️ Installation
1. Prerequisites

Ensure you have Python 3 installed.

Linux Users: You must install a system clipboard utility for the copy-paste feature to work:

    Wayland: sudo pacman -S wl-clipboard (Arch) or sudo apt install wl-clipboard (Debian/Ubuntu)

    X11: sudo pacman -S xclip (Arch) or sudo apt install xclip (Debian/Ubuntu)

2. Install Dependencies

Install the required Python packages:
Bash

pip install cryptography pyperclip

📖 Usage

Run the main script to start the application:
Bash

python main.py

First Run

    The application will detect that no database exists.

    You will be prompted to create a Master Password.

    Important: Remember this password. It is used to derive the encryption keys. If you lose it, your data is mathematically unrecoverable.

Main Menu

    [1] Add Password: Save a new credential. You will provide a Service Name (e.g., "Google"), a Username, and the Password.

    [2] Get Password: Retrieve a password. The decrypted password will be printed to the screen and automatically copied to your clipboard.

    [3] Generate Password: create a secure, random string of a specified length (letters + punctuation).

⚠️ Disclaimer

This tool is designed for personal use and educational purposes. While it implements strong, standard encryption algorithms (AES-GCM, PBKDF2), users should exercise standard security precautions:

    Do not share your passwords.db file.

    Use a strong Master Password.

    Ensure your machine is free of malware/keyloggers.

📄 License

MIT License
