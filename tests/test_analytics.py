"""Tests for consent-gated aggregate analytics."""

from datetime import UTC, datetime, timedelta

import pytest

from consent_input_lab.analytics import ConsentRequiredError, SessionAnalytics


def test_consent_required_before_session_start() -> None:
    analytics = SessionAnalytics()

    with pytest.raises(ConsentRequiredError):
        analytics.start_session()


def test_event_collection_only_while_active() -> None:
    analytics = SessionAnalytics()
    assert analytics.record_event("letter") is False

    analytics.set_consent(True)
    analytics.start_session(now=datetime(2026, 1, 1, tzinfo=UTC))
    assert analytics.record_event("letter") is True
    analytics.stop_session(now=datetime(2026, 1, 1, 0, 1, tzinfo=UTC))
    assert analytics.record_event("digit") is False

    summary = analytics.summary()
    assert summary.total_events == 1
    assert summary.counts_by_category["letter"] == 1
    assert summary.counts_by_category["digit"] == 0


def test_delete_current_session_clears_in_memory_data() -> None:
    analytics = SessionAnalytics()
    analytics.set_consent(True)
    analytics.start_session(now=datetime(2026, 1, 1, tzinfo=UTC))
    analytics.record_event("backspace")

    analytics.delete_current_session()

    summary = analytics.summary()
    assert summary.status == "Idle"
    assert summary.total_events == 0
    assert summary.backspace_count == 0
    assert summary.session_start is None
    assert summary.session_end is None


def test_typing_pace_uses_aggregate_counts_only() -> None:
    analytics = SessionAnalytics()
    analytics.set_consent(True)
    started = datetime(2026, 1, 1, tzinfo=UTC)
    analytics.start_session(now=started)
    analytics.record_event("letter")
    analytics.record_event("digit")

    pace = analytics.typing_pace_events_per_minute(now=started + timedelta(seconds=30))

    assert pace == 4.0
