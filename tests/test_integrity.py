"""Tests for SHA-256 export integrity."""

import json
from pathlib import Path

from consent_input_lab.integrity import (
    attach_digest,
    digest_payload,
    verify_json_export,
    verify_payload,
)


def test_sha256_digest_is_generated_correctly() -> None:
    payload = {"app_version": "1.0.0", "total_events": 3}
    with_digest = attach_digest(payload)

    assert with_digest["sha256_integrity_digest"] == digest_payload(payload)
    assert verify_payload(with_digest)


def test_integrity_verification_detects_modified_payload() -> None:
    payload = attach_digest({"app_version": "1.0.0", "total_events": 3})
    payload["total_events"] = 4

    assert verify_payload(payload) is False


def test_verify_json_export_detects_tampering(tmp_path: Path) -> None:
    path = tmp_path / "export.json"
    payload = attach_digest({"app_version": "1.0.0", "total_events": 3})
    path.write_text(json.dumps(payload), encoding="utf-8")
    assert verify_json_export(path)

    tampered = dict(payload)
    tampered["total_events"] = 99
    path.write_text(json.dumps(tampered), encoding="utf-8")
    assert not verify_json_export(path)
