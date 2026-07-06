"""Structured data models for privacy-safe input sessions."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Literal

APP_VERSION = "1.0.0"

EventCategory = Literal[
    "letter",
    "digit",
    "space",
    "backspace",
    "enter",
    "punctuation",
    "navigation",
    "modifier",
    "other",
]

EVENT_CATEGORIES: tuple[EventCategory, ...] = (
    "letter",
    "digit",
    "space",
    "backspace",
    "enter",
    "punctuation",
    "navigation",
    "modifier",
    "other",
)

SessionStatus = Literal["Idle", "Active", "Stopped"]


def utc_now() -> datetime:
    """Return a timezone-aware UTC timestamp."""
    return datetime.now(UTC)


def coarse_iso(timestamp: datetime | None) -> str | None:
    """Round a timestamp down to minute precision for privacy-safe exports."""
    if timestamp is None:
        return None
    normalized = timestamp.astimezone(UTC).replace(second=0, microsecond=0)
    return normalized.isoformat().replace("+00:00", "Z")


@dataclass(slots=True)
class SessionAggregates:
    """Aggregate-only session data with no raw input content."""

    counts: dict[EventCategory, int] = field(
        default_factory=lambda: {category: 0 for category in EVENT_CATEGORIES}
    )
    total_events: int = 0

    @property
    def backspace_count(self) -> int:
        """Return the aggregate backspace count."""
        return self.counts["backspace"]

    def record(self, category: EventCategory) -> None:
        """Increment aggregate counters for a categorized event."""
        self.counts[category] += 1
        self.total_events += 1

    def clear(self) -> None:
        """Reset all aggregate counters."""
        for category in EVENT_CATEGORIES:
            self.counts[category] = 0
        self.total_events = 0


@dataclass(slots=True)
class SessionState:
    """Consent-gated session state stored only in memory."""

    consent_given: bool = False
    status: SessionStatus = "Idle"
    started_at: datetime | None = None
    ended_at: datetime | None = None
    aggregates: SessionAggregates = field(default_factory=SessionAggregates)

    @property
    def is_active(self) -> bool:
        """Return whether a session is actively collecting aggregate events."""
        return self.status == "Active"
