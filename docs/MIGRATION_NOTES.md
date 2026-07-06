# Migration Notes

## Existing Features Discovered

The original repository tracked a single runnable script, `main.py`, plus generated artifacts: `log.txt`, `encrypted_log.dat`, and `secret.key`. The README described a system monitoring and reporting tool.

The legacy implementation contained:

- Global keyboard capture through `pynput.keyboard`.
- Mouse click tracking through `pynput.mouse`.
- Active-window and process-name collection on Windows.
- Screenshot capture through `pyautogui`.
- Local raw log files.
- Fernet encryption of collected logs using a generated `secret.key`.
- SMTP email delivery with encrypted logs, raw log content, screenshots, username, and IP-related data.
- Cleanup logic for generated logs and screenshots.
- Windows Registry startup persistence.
- Hidden console behavior.
- Mutex-based single-instance behavior.
- Broad exception swallowing.

## Safe Concepts Retained or Redesigned

- Event categorization was retained but redesigned to classify only events typed inside the app's own practice text field.
- Local session lifecycle was retained as explicit Start, Stop, Delete, and Export actions.
- Error handling was redesigned to use explicit exceptions and user-visible messages instead of broad silent failures.
- Configuration was moved into standard project metadata and small cohesive modules.
- Integrity verification was retained conceptually but redesigned as SHA-256 tamper-evidence for aggregate export payloads.
- Local analytics were retained only as aggregate counts and pace estimates.

## Unsafe Capabilities Removed

- Global keyboard hooks were removed because the final app must not capture input outside its own visible text field.
- Raw typed-content logging was removed because it can expose credentials, private messages, and sensitive personal data.
- Active-window and process tracking were removed because they reveal user behavior outside the app.
- Mouse tracking was removed because pointer coordinates can reveal private workflows.
- Screenshots were removed because they can capture unrelated private information.
- SMTP and remote reporting were removed because the final app must be local-only and must not exfiltrate data.
- Username, IP, host, and environment credential handling were removed because they are unnecessary for aggregate local analytics.
- Windows Registry persistence, hidden console behavior, and mutex-based covert execution were removed because the app must be visible and user-controlled.
- Generated artifacts `log.txt`, `encrypted_log.dat`, and `secret.key` were removed from the working tree and ignored going forward.

## Resulting Direction

The repository is now a consent-based portfolio lab focused on secure software engineering, data minimization, local-only analytics, testability, documentation, and threat modeling.
