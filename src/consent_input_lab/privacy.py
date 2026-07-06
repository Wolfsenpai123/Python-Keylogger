"""Privacy-preserving input event classification."""

from __future__ import annotations

import string

from consent_input_lab.models import EventCategory

_NAVIGATION_KEYS = {
    "Left",
    "Right",
    "Up",
    "Down",
    "Home",
    "End",
    "Prior",
    "Next",
    "Page_Up",
    "Page_Down",
}

_MODIFIER_KEYS = {
    "Shift_L",
    "Shift_R",
    "Control_L",
    "Control_R",
    "Alt_L",
    "Alt_R",
    "Meta_L",
    "Meta_R",
    "Super_L",
    "Super_R",
    "Caps_Lock",
}

_ENTER_KEYS = {"Return", "KP_Enter"}


def classify_key_event(keysym: str, char: str | None) -> EventCategory:
    """Classify a Tkinter key event without returning raw typed content."""
    if keysym == "BackSpace":
        return "backspace"
    if keysym in _ENTER_KEYS:
        return "enter"
    if keysym in _NAVIGATION_KEYS:
        return "navigation"
    if keysym in _MODIFIER_KEYS:
        return "modifier"

    if char == " ":
        return "space"
    if char is None or char == "":
        return "other"
    if len(char) != 1:
        return "other"
    if char.isalpha():
        return "letter"
    if char.isdigit():
        return "digit"
    if char in string.punctuation:
        return "punctuation"
    return "other"
