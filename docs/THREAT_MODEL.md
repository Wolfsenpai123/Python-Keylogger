# Threat Model

## Assets to Protect

- Raw typed content entered by the user.
- User consent and control over collection.
- Local aggregate session summaries.
- Integrity of exported JSON summaries.
- The user's broader desktop activity outside the app.

## Threat Actors

- A curious local user reading files in the project directory.
- A malicious maintainer attempting to reintroduce surveillance behavior.
- A user who misunderstands what the tool collects.
- Malware or another local process with access to the same filesystem.

## Trust Boundaries

- The application boundary is the visible Tkinter process.
- The input boundary is the app's own practice text field.
- The data boundary is in-memory aggregates and explicit local exports under `data/exports/`.
- The repository boundary excludes generated secrets, screenshots, raw logs, and remote credentials.

## Abuse Cases Intentionally Prevented

- Capturing global keystrokes from other applications.
- Reconstructing words, passwords, or sentences from raw key logs.
- Tracking active windows, process names, mouse clicks, or screen contents.
- Running hidden in the background.
- Starting automatically through Registry keys or scheduled tasks.
- Sending activity data through SMTP, webhooks, sockets, or HTTP requests.
- Collecting credentials, usernames, IP addresses, machine identifiers, or browser data.

## Privacy Risks

- The practice text field can visibly contain what the user typed during a session.
- Exported aggregate summaries reveal approximate activity volume and coarse timing.
- A local attacker with filesystem access can read exported summaries.
- SHA-256 integrity detects accidental or unsophisticated tampering but does not prove authorship.

## Mitigations

- Consent is required before a session can start.
- Collection is limited to in-app key events from the practice text field.
- Events are immediately reduced to categories.
- Session data is aggregate-only and in memory until explicit export.
- Export payloads are allowlisted.
- Generated exports are local-only and ignored by Git.
- Delete Current Session clears aggregate session state and the visible practice field.
- Documentation states non-goals and unsafe behavior that must not be reintroduced.
- Unit tests cover consent gating, active-session collection, export allowlisting, and integrity verification.

## Residual Risks and Limitations

- The app cannot protect exports from someone who already has local filesystem access.
- The digest is not authentication, encryption, or a digital signature.
- The app does not securely wipe disk blocks because it does not automatically delete prior exports.
- Tkinter text remains visible while the user is typing, as expected for an interactive practice field.
- The threat model depends on future maintainers preserving the no-surveillance boundaries.
