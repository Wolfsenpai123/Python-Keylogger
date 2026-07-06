"""Consent-gated aggregate analytics for local sessions."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from consent_input_lab.models import (
    EVENT_CATEGORIES,
    EventCategory,
    SessionState,
    coarse_iso,
    utc_now,
)


@dataclass(slots=True)
class SessionSummary:
    """Exportable aggregate session summary."""

    consent_recorded: bool
    status: str
    session_start: str | None
    session_end: str | None
    duration_seconds: int
    total_events: int
    counts_by_category: dict[EventCategory, int]
    backspace_count: int
    typing_pace_events_per_minute: float


class ConsentRequiredError(ValueError):
    """Raised when a session starts before consent is recorded."""


class SessionAnalytics:
    """Manage consent, lifecycle state, and aggregate-only input analytics."""

    def __init__(self) -> None:
        self.state = SessionState()

    def set_consent(self, consent_given: bool) -> None:
        """Record whether the visible consent checkbox is selected."""
        self.state.consent_given = consent_given

    def start_session(self, *, now: datetime | None = None) -> None:
        """Start aggregate collection only after explicit consent."""
        if not self.state.consent_given:
            raise ConsentRequiredError("Consent is required before starting a session.")
        self.state.status = "Active"
        self.state.started_at = now or utc_now()
        self.state.ended_at = None
        self.state.aggregates.clear()

    def stop_session(self, *, now: datetime | None = None) -> None:
        """Stop collection while retaining aggregate counts for review/export."""
        if self.state.status == "Active":
            self.state.ended_at = now or utc_now()
            self.state.status = "Stopped"

    def delete_current_session(self) -> None:
        """Clear in-memory session aggregates and lifecycle timestamps."""
        self.state.aggregates.clear()
        self.state.started_at = None
        self.state.ended_at = None
        self.state.status = "Idle"

    def record_event(self, category: EventCategory) -> bool:
        """Record a categorized event only while the session is active."""
        if not self.state.is_active:
            return False
        self.state.aggregates.record(category)
        return True

    def duration_seconds(self, *, now: datetime | None = None) -> int:
        """Return coarse session duration in whole seconds."""
        if self.state.started_at is None:
            return 0
        end_time = self.state.ended_at or now or utc_now()
        return max(0, int((end_time - self.state.started_at).total_seconds()))

    def typing_pace_events_per_minute(self, *, now: datetime | None = None) -> float:
        """Estimate aggregate pace from total event count and session duration."""
        duration = self.duration_seconds(now=now)
        if duration == 0:
            return 0.0
        return round(self.state.aggregates.total_events / (duration / 60), 2)

    def summary(self, *, now: datetime | None = None) -> SessionSummary:
        """Return an aggregate-only summary suitable for display or export."""
        counts = {category: self.state.aggregates.counts[category] for category in EVENT_CATEGORIES}
        return SessionSummary(
            consent_recorded=self.state.consent_given,
            status=self.state.status,
            session_start=coarse_iso(self.state.started_at),
            session_end=coarse_iso(self.state.ended_at),
            duration_seconds=self.duration_seconds(now=now),
            total_events=self.state.aggregates.total_events,
            counts_by_category=counts,
            backspace_count=self.state.aggregates.backspace_count,
            typing_pace_events_per_minute=self.typing_pace_events_per_minute(now=now),
        )
