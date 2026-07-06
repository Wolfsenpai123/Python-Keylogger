"""Tests for privacy-safe event classification."""

from consent_input_lab.privacy import classify_key_event


def test_event_classification_categories() -> None:
    assert classify_key_event("a", "a") == "letter"
    assert classify_key_event("1", "1") == "digit"
    assert classify_key_event("space", " ") == "space"
    assert classify_key_event("BackSpace", "\x08") == "backspace"
    assert classify_key_event("Return", "\r") == "enter"
    assert classify_key_event("period", ".") == "punctuation"
    assert classify_key_event("Left", "") == "navigation"
    assert classify_key_event("Shift_L", "") == "modifier"
    assert classify_key_event("F5", "") == "other"
