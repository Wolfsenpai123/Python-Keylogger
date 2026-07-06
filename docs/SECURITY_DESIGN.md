# Security Design

## Secure-by-Default Decisions

- The application starts idle.
- The Start Session button is disabled until explicit consent is selected.
- Collection happens only in the visible practice text field.
- No network client, SMTP client, webhook client, socket client, or HTTP client is implemented.
- No global keyboard hook, mouse hook, screenshot capture, active-window query, or clipboard read is implemented.
- No background stealth mode, persistence, startup registration, or hidden console behavior is implemented.
- Exports are created only after an explicit user action.

## Data Minimization Rules

- Do not store raw typed text.
- Do not store exact key sequences that could reconstruct sensitive input.
- Do not store window titles, process names, usernames, IP addresses, machine identifiers, system paths, screenshots, or clipboard data.
- Keep only event category counts, total event count, backspace count, duration, pace, app version, coarse session timestamps, export creation time, and digest.
- Use coarse minute-level ISO timestamps for exported session start and end values.

## Export Integrity Design

The exporter builds an allowlisted aggregate payload and then computes a SHA-256 digest over a deterministic JSON serialization of that payload without the digest field. The digest is stored as `sha256_integrity_digest`.

Verification loads a JSON export, removes the digest field, recalculates the digest, and compares it with the recorded value using constant-time comparison.

This provides tamper-evidence for the exported payload. It does not provide authentication, authorization, non-repudiation, confidentiality, or encryption. Anyone who can modify the file can also recalculate the digest unless an external trusted copy exists.

## Deletion Behavior

Delete Current Session clears in-memory aggregate counters, session timestamps, the status indicator, and the visible practice text field. It does not automatically delete exports because exports are explicit user-created files. The UI tells users to manually remove files from `data/exports/` when they no longer need them.

## Why This Is Safer Than the Original Architecture

The original architecture collected broad user activity, including global keystrokes, mouse clicks, screenshots, active-window/process metadata, usernames, IP-related data, and remote SMTP reports. It also attempted stealth and persistence through hidden execution and startup registration.

The redesigned architecture is visible, consent-based, local-only, and aggregate-only. It avoids surveillance primitives entirely and turns the project into a demonstrable secure engineering lab with tests, documentation, threat modeling, and clear privacy boundaries.
