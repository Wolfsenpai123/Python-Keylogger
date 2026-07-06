"""Application entry point."""

from __future__ import annotations

from consent_input_lab.ui import ConsentInputLabApp


def main() -> None:
    """Run the visible consent-based desktop application."""
    app = ConsentInputLabApp()
    app.mainloop()


if __name__ == "__main__":
    main()
