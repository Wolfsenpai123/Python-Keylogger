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
```
Here is the complete content for your README.md file in English. I have consolidated everything into a single code block for you to copy and paste directly into your project.

Markdown
# System Monitoring & Security Research Tool (SMSA)

## 📌 Project Overview
This project is an integrated system monitoring tool developed in Python for educational and research purposes. It focuses on system data collection, secure data encryption, and remote reporting within the framework of **CyberOps** and **Network Security** studies.

The tool simulates the functionality of a security management agent by logging user interactions, capturing visual state data, and transmitting reports securely via SMTP.

---

## ✨ Key Features

### 1. Activity Monitoring
* **Keystroke Logging:** Records every keypress along with timestamps and the name of the active window/process.
* **Mouse Tracking:** Logs mouse click coordinates to analyze user interaction patterns.
* **Periodic Screenshots:** Automatically captures the desktop at configurable intervals to monitor visual activity.

### 2. Security & Data Integrity
* **AES Encryption:** Utilizes the **Fernet (Symmetric Encryption)** scheme to encrypt log files, protecting data from unauthorized local access.
* **Credential Protection:** Retrieves sensitive information (Email/Password) from system environment variables instead of hardcoding them, preventing data leaks.
* **Secure Reporting:** Automatically packages encrypted logs and the latest screenshots into an email sent via SMTP (Gmail).
* **Automated Cleanup:** Manages storage by deleting logs and screenshots older than a specified threshold (e.g., 7 days).

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
```
## 🚀 Getting Started

### 1. System Requirements
Operating System: Windows 10/11 (Required for persistence and stealth features).

Python: Version 3.8 or higher.

### 2. Installation
Install the necessary dependencies using pip:

Bash
```
pip install pynput pyautogui cryptography psutil pywin32
```
### 3. Configuration (Secure Setup)
To protect your privacy, this script retrieves credentials from your system's environment variables.

Set up environment variables on Windows:

Open Command Prompt (CMD) or PowerShell.

Run the following commands (replace with your actual data):

DOS
setx MY_APP_EMAIL "your_email@gmail.com"
setx MY_APP_PASSWORD "your_google_app_password"
setx MY_APP_RECEIVER "receiver_email@gmail.com"
Note: You must use a Google App Password for the MY_APP_PASSWORD variable. Restart your IDE (VS Code/PyCharm) after setting these variables.

## ⚖️ Disclaimer
This project is created strictly for educational purposes and academic research at FPT University.

DO NOT use this tool for illegal activities or unauthorized system access.

Monitoring a computer without the explicit consent of the owner is a violation of privacy laws.

The author is not responsible for any misuse or damage caused by this source code.

### 👤 Author
Phan Thiện Quang

Institution: FPT University

Field of Study: Network Security / CyberOps


### 💡 Quick Checklist for your `main.py`:
1.  **Remove Duplicates:** Ensure you have deleted the second `take_screenshot()` function at the bottom of your script (the one with the indentation error).
2.  **Update Config:** Make sure the top of your script uses `os.environ.get('MY_APP_EMAIL')` and the other variables mentioned in the README.
3.  **App Password:** Double-check that you are using a 16-character Google App Password, as a re
