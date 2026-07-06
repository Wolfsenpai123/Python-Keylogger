"""Tests for local allowlisted exports."""

from datetime import UTC, datetime
from pathlib import Path

from consent_input_lab.analytics import SessionAnalytics, SessionSummary
from consent_input_lab.exporter import ALLOWED_EXPORT_FIELDS, LocalExporter, build_export_payload
from consent_input_lab.integrity import verify_payload


def _summary_with_events() -> SessionSummary:
    analytics = SessionAnalytics()
    analytics.set_consent(True)
    analytics.start_session(now=datetime(2026, 1, 1, 12, 34, 56, tzinfo=UTC))
    analytics.record_event("letter")
    analytics.record_event("space")
    analytics.record_event("backspace")
    analytics.stop_session(now=datetime(2026, 1, 1, 12, 35, 56, tzinfo=UTC))
    return analytics.summary()


def test_export_contains_only_allowlisted_aggregate_fields() -> None:
    payload = build_export_payload(
        _summary_with_events(), now=datetime(2026, 1, 1, 12, 36, tzinfo=UTC)
    )

    assert set(payload) == ALLOWED_EXPORT_FIELDS
    assert set(payload["counts_by_category"]) == {
        "letter",
        "digit",
        "space",
        "backspace",
        "enter",
        "punctuation",
        "navigation",
        "modifier",
        "other",
    }
    forbidden_names = {
        "raw",
        "text",
        "key",
        "window",
        "process",
        "clipboard",
        "screenshot",
        "username",
        "ip",
    }
    assert forbidden_names.isdisjoint({field.lower() for field in payload})
    assert verify_payload(payload)


def test_export_writes_json_and_csv_locally(tmp_path: Path) -> None:
    exporter = LocalExporter(tmp_path)

    json_path, csv_path = exporter.export(
        _summary_with_events(), now=datetime(2026, 1, 1, 12, 36, tzinfo=UTC)
    )

    assert json_path.exists()
    assert csv_path.exists()
    assert json_path.parent == tmp_path
    assert csv_path.parent == tmp_path
    assert (
        "letter"
        not in json_path.read_text(encoding="utf-8").lower().split("counts_by_category", 1)[0]
    )


def test_no_raw_typed_text_is_persisted_in_export_payload() -> None:
    payload = build_export_payload(
        _summary_with_events(), now=datetime(2026, 1, 1, 12, 36, tzinfo=UTC)
    )
    serialized = str(payload).lower()

    assert "password" not in serialized
    assert "hello" not in serialized
    assert "typed_text" not in serialized
