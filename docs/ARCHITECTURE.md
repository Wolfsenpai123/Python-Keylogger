# Architecture

## Diagram

```text
+-------------------------------+
| Tkinter UI                    |
| consent, buttons, text field  |
+---------------+---------------+
                |
                | in-app key event only after Start Session
                v
+---------------+---------------+
| privacy.py                    |
| classify into safe category   |
+---------------+---------------+
                |
                | category only
                v
+---------------+---------------+
| analytics.py / models.py      |
| in-memory aggregates          |
+---------------+---------------+
                |
                | explicit Export click
                v
+---------------+---------------+
| exporter.py                   |
| allowlisted JSON and CSV      |
+---------------+---------------+
                |
                | digest payload
                v
+---------------+---------------+
| integrity.py                  |
| SHA-256 tamper-evidence       |
+---------------+---------------+
                |
                v
        data/exports/ local files
```

## Data Flow

1. The user opens a visible Tkinter desktop application.
2. The Start Session button stays disabled until the user selects the consent checkbox.
3. After Start Session, the app listens only to key events from its own practice text field.
4. Each event is immediately converted into a privacy-safe category.
5. Only aggregate counters are kept in memory.
6. The user may stop the session, delete the current in-memory session, or explicitly export a summary.
7. Exports are written only to `data/exports/` as JSON and CSV.
8. JSON exports include a SHA-256 digest that can be verified later.

## Module Responsibilities

- `app.py`: starts the desktop application.
- `ui.py`: owns the visible Tkinter widgets, consent gating, buttons, messages, and chart.
- `privacy.py`: maps Tkinter key events to coarse categories without exposing raw typed content.
- `analytics.py`: manages consent, active/stopped/idle state, duration, counts, and pace.
- `models.py`: defines dataclasses, event category types, app version, and coarse timestamp helpers.
- `exporter.py`: builds allowlisted aggregate payloads and writes local JSON/CSV files.
- `integrity.py`: creates and verifies SHA-256 digests for JSON-compatible payloads.

## Privacy Boundary

The privacy boundary is the practice text field. The application does not install global hooks and does not observe other applications. Inside the boundary, key events are converted into categories immediately. Raw typed content is not copied into session models, analytics, exports, logs, or integrity payloads.

The visible text field may still display what the user types as normal UI state. That content is cleared when Delete Current Session is clicked and is never exported by the application.
