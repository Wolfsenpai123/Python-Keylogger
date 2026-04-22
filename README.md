# System Monitoring & Security Research Tool (SMSA)

## 📌 Overview
This project is an integrated system monitoring tool developed in Python for educational and research purposes. It focuses on system data collection, secure data encryption, and remote reporting within the framework of **CyberOps** and **Network Security** studies.

The tool simulates the functionality of a security management agent by logging user interactions, capturing visual state data, and transmitting reports securely via SMTP.

---

## ✨ Key Features

### 1. Activity Monitoring
* **Keystroke Logging:** Records every keypress along with timestamps and the name of the active window/process.
* **Mouse Tracking:** Logs mouse click coordinates to analyze user interaction patterns.
* **Periodic Screenshots:** Automatically captures the desktop at configurable intervals (default: 5 minutes).

### 2. Security & Data Integrity
* **AES Encryption:** Utilizes the **Fernet (Symmetric Encryption)** scheme to encrypt log files, protecting data from unauthorized local access.
* **Environment Variable Integration:** Credentials are kept secure by using system environment variables instead of hardcoded strings.
* **Secure Reporting:** Automatically packages encrypted logs and the latest screenshots into an email sent via SMTP.
* **Automated Cleanup:** Manages storage by deleting logs and screenshots older than a specified threshold (default: 7 days).

### 3. Stealth & Persistence
* **Persistence:** Automatically registers with the Windows Registry (`Run` key) to ensure the tool starts upon system boot.
* **Stealth Mode:** Operates as a background process by hiding the console window on Windows systems.
* **Single Instance Protection:** Uses a system-wide **Mutex** to prevent multiple instances of the tool from running simultaneously.

---

## 🛠 Project Structure
```text
.
├── main.py                # Core execution script
├── secret.key             # Encryption key (auto-generated)
├── log.txt                # Local temporary log file
├── encrypted_log.dat      # Encrypted log file for transmission
└── screenshots/           # Directory for captured screen images
