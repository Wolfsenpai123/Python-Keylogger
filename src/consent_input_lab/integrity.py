"""SHA-256 export integrity helpers."""

from __future__ import annotations

import hashlib
import hmac
import json
from pathlib import Path
from typing import Any

DIGEST_FIELD = "sha256_integrity_digest"


def canonical_json_bytes(payload: dict[str, Any]) -> bytes:
    """Serialize a payload deterministically for digest calculation."""
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


def digest_payload(payload: dict[str, Any]) -> str:
    """Return a SHA-256 digest for a JSON-serializable payload."""
    return hashlib.sha256(canonical_json_bytes(payload)).hexdigest()


def attach_digest(payload: dict[str, Any]) -> dict[str, Any]:
    """Return a copy of the payload with its integrity digest attached."""
    payload_without_digest = {key: value for key, value in payload.items() if key != DIGEST_FIELD}
    with_digest = dict(payload_without_digest)
    with_digest[DIGEST_FIELD] = digest_payload(payload_without_digest)
    return with_digest


def verify_payload(payload: dict[str, Any]) -> bool:
    """Verify the attached SHA-256 digest for a decoded export payload."""
    recorded_digest = payload.get(DIGEST_FIELD)
    if not isinstance(recorded_digest, str):
        return False
    payload_without_digest = {key: value for key, value in payload.items() if key != DIGEST_FIELD}
    expected_digest = digest_payload(payload_without_digest)
    return hmac.compare_digest(recorded_digest, expected_digest)


def verify_json_export(path: Path) -> bool:
    """Verify an exported JSON summary from disk."""
    with path.open("r", encoding="utf-8") as export_file:
        payload = json.load(export_file)
    if not isinstance(payload, dict):
        return False
    return verify_payload(payload)
