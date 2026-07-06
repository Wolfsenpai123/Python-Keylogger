# Consent-Based Input Security Lab

Consent-Based Input Security Lab is a local-only Python desktop application that demonstrates privacy-by-design input analytics. It uses a visible Tkinter interface, requires explicit consent before a session can begin, and records only aggregate event categories from the app's own practice text field.

This repository was redesigned from an earlier educational monitoring script into a safer cybersecurity portfolio project. The new architecture keeps defensible learning goals such as event categorization, local session lifecycle, aggregate analytics, and integrity verification while removing unsafe monitoring, stealth, persistence, screenshots, and remote reporting behavior.

## Features

- Consent-first interface with a mandatory checkbox before session start.
- Controlled practice text field inside the application.
- Event categories only: letter, digit, space, backspace, enter, punctuation, navigation, modifier, and other.
- Live aggregate metrics for duration, total events, category counts, backspaces, and typing pace.
- Basic Tkinter Canvas summary chart.
- User-controlled JSON and CSV export to `data/exports/`.
- SHA-256 digest for tamper-evidence of exported JSON payloads.
- JSON export verification tool in the UI.
- In-memory session deletion that clears visible metrics and the practice field.
- Unit tests for privacy, analytics, exporting, and integrity.

## Privacy Guarantees

The application does not store raw typed content. It does not capture input outside its own text field. It does not read the clipboard, take screenshots, inspect active windows, collect process names, collect usernames, collect IP addresses, generate machine identifiers, install persistence, hide itself, or send data over a network.

Exports are local files created only after the user clicks Export Summary. They contain aggregate counts, coarse session timestamps, an aggregate pace estimate, app version, export creation time, and a SHA-256 integrity digest.

## Non-Goals

- No global key capture.
- No stealth mode.
- No persistence or auto-start.
- No screenshots or screen recording.
- No mouse tracking.
- No clipboard access.
- No remote reporting, SMTP, webhooks, sockets, or HTTP requests.
- No credential collection.
- No surveillance or background monitoring.

## Installation

Python 3.11 or newer is required.

```bash
python -m pip install -e ".[dev]"
```

If you use `just`, the same setup is available as:

```bash
just install
```

## Run

```bash
PYTHONPATH=src python -m consent_input_lab.app
```

Or, after installation:

```bash
consent-input-lab
```

With `just`:

```bash
just run
```

## Test and Lint

```bash
PYTHONPATH=src pytest
ruff check .
ruff format .
```

With `just`:

```bash
just test
just lint
just format
```

## Architecture Overview

The app is split into small modules under `src/consent_input_lab/`:

- `app.py`: desktop entry point.
- `ui.py`: Tkinter interface, consent controls, local export and verification buttons.
- `analytics.py`: consent-gated session lifecycle and aggregate metrics.
- `privacy.py`: input event classification into safe categories.
- `models.py`: dataclasses and shared constants.
- `exporter.py`: allowlisted local JSON and CSV exports.
- `integrity.py`: SHA-256 digest generation and verification.

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), [docs/SECURITY_DESIGN.md](docs/SECURITY_DESIGN.md), and [docs/THREAT_MODEL.md](docs/THREAT_MODEL.md) for more detail.

## Threat-Model Summary

The primary assets are typed content, user privacy, local export integrity, and user consent. The design prevents common abuse paths by avoiding global hooks, stealth execution, persistence, remote delivery, screenshots, clipboard access, and active-window inspection. Residual risks include local filesystem access by someone who can read exported summaries, shoulder-surfing of visible text in the practice field, and the fact that SHA-256 provides tamper-evidence but not authentication or encryption.

## Screenshot Placeholder

Add a manual screenshot here only if you choose to document the visible application UI. The application does not generate or collect screenshots automatically.

## What I Learned

This project demonstrates how to turn a risky monitoring concept into a consent-based security lab. The redesign applies data minimization, explicit consent, local-only processing, structured testing, tamper-evident exports, and threat modeling. It shows that cybersecurity engineering is not just about collecting signals; it is about defining safe boundaries, limiting abuse potential, documenting tradeoffs, and testing privacy guarantees.
