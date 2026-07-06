"""User-controlled local exports for aggregate summaries."""

from __future__ import annotations

import csv
import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Any

from consent_input_lab.analytics import SessionSummary
from consent_input_lab.integrity import attach_digest
from consent_input_lab.models import APP_VERSION, EVENT_CATEGORIES, coarse_iso, utc_now

DEFAULT_EXPORT_DIR = Path("data") / "exports"

ALLOWED_EXPORT_FIELDS = {
    "app_version",
    "consent_recorded",
    "session_start",
    "session_end",
    "duration_seconds",
    "total_events",
    "counts_by_category",
    "backspace_count",
    "typing_pace_events_per_minute",
    "export_created_at",
    "sha256_integrity_digest",
}


def build_export_payload(summary: SessionSummary, *, now: datetime | None = None) -> dict[str, Any]:
    """Build an allowlisted aggregate export payload with an integrity digest."""
    summary_data = asdict(summary)
    payload: dict[str, Any] = {
        "app_version": APP_VERSION,
        "consent_recorded": bool(summary_data["consent_recorded"]),
        "session_start": summary_data["session_start"],
        "session_end": summary_data["session_end"],
        "duration_seconds": int(summary_data["duration_seconds"]),
        "total_events": int(summary_data["total_events"]),
        "counts_by_category": {
            category: int(summary.counts_by_category[category]) for category in EVENT_CATEGORIES
        },
        "backspace_count": int(summary_data["backspace_count"]),
        "typing_pace_events_per_minute": float(summary_data["typing_pace_events_per_minute"]),
        "export_created_at": coarse_iso(now or utc_now()),
    }
    return attach_digest(payload)


def validate_export_payload(payload: dict[str, Any]) -> None:
    """Reject payloads that contain fields outside the privacy allowlist."""
    extra_fields = set(payload) - ALLOWED_EXPORT_FIELDS
    if extra_fields:
        raise ValueError(f"Export payload contains disallowed fields: {sorted(extra_fields)}")
    missing_fields = ALLOWED_EXPORT_FIELDS - set(payload)
    if missing_fields:
        raise ValueError(f"Export payload is missing required fields: {sorted(missing_fields)}")
    if payload["consent_recorded"] is not True:
        raise ValueError("Exports require a consent-recorded session summary.")


class LocalExporter:
    """Write aggregate summaries to local JSON and CSV files on explicit request."""

    def __init__(self, export_dir: Path = DEFAULT_EXPORT_DIR) -> None:
        self.export_dir = export_dir

    def export(self, summary: SessionSummary, *, now: datetime | None = None) -> tuple[Path, Path]:
        """Create JSON and CSV aggregate exports in the local export directory."""
        payload = build_export_payload(summary, now=now)
        validate_export_payload(payload)
        self.export_dir.mkdir(parents=True, exist_ok=True)
        stamp = (now or utc_now()).strftime("%Y%m%d_%H%M%S")
        json_path = self.export_dir / f"session_summary_{stamp}.json"
        csv_path = self.export_dir / f"session_summary_{stamp}.csv"
        self._write_json(json_path, payload)
        self._write_csv(csv_path, payload)
        return json_path, csv_path

    @staticmethod
    def _write_json(path: Path, payload: dict[str, Any]) -> None:
        with path.open("w", encoding="utf-8") as json_file:
            json.dump(payload, json_file, indent=2, sort_keys=True)
            json_file.write("\n")

    @staticmethod
    def _write_csv(path: Path, payload: dict[str, Any]) -> None:
        flat_row = {
            "app_version": payload["app_version"],
            "consent_recorded": payload["consent_recorded"],
            "session_start": payload["session_start"],
            "session_end": payload["session_end"],
            "duration_seconds": payload["duration_seconds"],
            "total_events": payload["total_events"],
            "backspace_count": payload["backspace_count"],
            "typing_pace_events_per_minute": payload["typing_pace_events_per_minute"],
            "export_created_at": payload["export_created_at"],
            "sha256_integrity_digest": payload["sha256_integrity_digest"],
        }
        for category in EVENT_CATEGORIES:
            flat_row[f"count_{category}"] = payload["counts_by_category"][category]
        with path.open("w", encoding="utf-8", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=list(flat_row))
            writer.writeheader()
            writer.writerow(flat_row)
