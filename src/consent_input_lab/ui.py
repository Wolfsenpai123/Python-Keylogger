"""Tkinter user interface for the consent-based input lab."""

from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from consent_input_lab.analytics import ConsentRequiredError, SessionAnalytics
from consent_input_lab.exporter import LocalExporter
from consent_input_lab.integrity import verify_json_export
from consent_input_lab.models import APP_VERSION, EVENT_CATEGORIES
from consent_input_lab.privacy import classify_key_event


class ConsentInputLabApp(tk.Tk):
    """Visible desktop app that records only aggregate in-app input categories."""

    def __init__(self, analytics: SessionAnalytics | None = None) -> None:
        super().__init__()
        self.title(f"Consent-Based Input Security Lab v{APP_VERSION}")
        self.geometry("980x720")
        self.minsize(820, 620)
        self.analytics = analytics or SessionAnalytics()
        self.exporter = LocalExporter()
        self.consent_var = tk.BooleanVar(value=False)
        self.status_var = tk.StringVar(value="Idle")
        self.message_var = tk.StringVar(
            value="Review the privacy notice and provide consent to begin."
        )
        self.metric_vars: dict[str, tk.StringVar] = {}
        self.category_vars = {category: tk.StringVar(value="0") for category in EVENT_CATEGORIES}
        self._build_ui()
        self._refresh_metrics()

    def _build_ui(self) -> None:
        root = ttk.Frame(self, padding=16)
        root.grid(row=0, column=0, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=2)
        root.columnconfigure(1, weight=1)
        root.rowconfigure(3, weight=1)

        title = ttk.Label(
            root, text="Consent-Based Input Security Lab", font=("TkDefaultFont", 18, "bold")
        )
        title.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))

        privacy_text = (
            "This local desktop lab demonstrates privacy-safe input analytics. "
            "It captures events only inside the practice text field after you start "
            "a consented session. It never records raw text, screenshots, clipboard "
            "contents, active windows, or sends data online."
        )
        privacy = ttk.Label(root, text=privacy_text, wraplength=880, justify="left")
        privacy.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 12))

        controls = ttk.Frame(root)
        controls.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 12))
        controls.columnconfigure(6, weight=1)

        consent = ttk.Checkbutton(
            controls,
            text="I consent to local aggregate-only input analytics in this application.",
            variable=self.consent_var,
            command=self._on_consent_change,
        )
        consent.grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 8))

        self.start_button = ttk.Button(
            controls, text="Start Session", command=self._start_session, state="disabled"
        )
        self.start_button.grid(row=1, column=0, padx=(0, 8))
        self.stop_button = ttk.Button(controls, text="Stop Session", command=self._stop_session)
        self.stop_button.grid(row=1, column=1, padx=(0, 8))
        self.delete_button = ttk.Button(
            controls, text="Delete Current Session", command=self._delete_session
        )
        self.delete_button.grid(row=1, column=2, padx=(0, 8))
        self.export_button = ttk.Button(
            controls, text="Export Summary", command=self._export_summary
        )
        self.export_button.grid(row=1, column=3, padx=(0, 8))
        verify_button = ttk.Button(controls, text="Verify JSON Export", command=self._verify_export)
        verify_button.grid(row=1, column=4, padx=(0, 8))

        status_label = ttk.Label(
            controls, textvariable=self.status_var, font=("TkDefaultFont", 12, "bold")
        )
        status_label.grid(row=1, column=5, padx=(16, 0), sticky="e")

        main = ttk.PanedWindow(root, orient=tk.HORIZONTAL)
        main.grid(row=3, column=0, columnspan=2, sticky="nsew")

        left = ttk.Frame(main, padding=(0, 0, 12, 0))
        right = ttk.Frame(main)
        main.add(left, weight=3)
        main.add(right, weight=2)
        left.rowconfigure(1, weight=1)
        left.columnconfigure(0, weight=1)
        right.columnconfigure(0, weight=1)

        warning = ttk.Label(
            left,
            text="Practice field: only category counts are collected while the session is Active.",
            wraplength=540,
            justify="left",
        )
        warning.grid(row=0, column=0, sticky="ew", pady=(0, 6))

        self.practice_text = tk.Text(left, height=14, wrap="word", undo=False)
        self.practice_text.grid(row=1, column=0, sticky="nsew")
        self.practice_text.bind("<KeyPress>", self._on_key_press)
        self.practice_text.bind("<<Paste>>", self._block_paste)

        self.message_label = ttk.Label(
            left, textvariable=self.message_var, wraplength=540, justify="left"
        )
        self.message_label.grid(row=2, column=0, sticky="ew", pady=(10, 0))

        metrics = ttk.LabelFrame(right, text="Live Aggregate Metrics", padding=10)
        metrics.grid(row=0, column=0, sticky="ew")
        for index, label in enumerate(("Duration", "Total events", "Backspaces", "Pace")):
            self.metric_vars[label] = tk.StringVar(value="0")
            ttk.Label(metrics, text=label).grid(row=index, column=0, sticky="w", pady=2)
            ttk.Label(metrics, textvariable=self.metric_vars[label]).grid(
                row=index, column=1, sticky="e", pady=2
            )
        metrics.columnconfigure(1, weight=1)

        category_frame = ttk.LabelFrame(right, text="Counts by Category", padding=10)
        category_frame.grid(row=1, column=0, sticky="ew", pady=(12, 0))
        category_frame.columnconfigure(1, weight=1)
        for index, category in enumerate(EVENT_CATEGORIES):
            ttk.Label(category_frame, text=category).grid(row=index, column=0, sticky="w", pady=1)
            ttk.Label(category_frame, textvariable=self.category_vars[category]).grid(
                row=index, column=1, sticky="e", pady=1
            )

        visual_frame = ttk.LabelFrame(right, text="Visual Summary", padding=10)
        visual_frame.grid(row=2, column=0, sticky="ew", pady=(12, 0))
        self.canvas = tk.Canvas(
            visual_frame, height=180, background="#ffffff", highlightthickness=1
        )
        self.canvas.grid(row=0, column=0, sticky="ew")
        visual_frame.columnconfigure(0, weight=1)

        health = ttk.LabelFrame(right, text="Session Health / Privacy", padding=10)
        health.grid(row=3, column=0, sticky="ew", pady=(12, 0))
        health_text = (
            "Local only. Consent required. Aggregate categories only. No raw text, "
            "clipboard, screenshots, active-window data, persistence, or network reporting."
        )
        ttk.Label(health, text=health_text, wraplength=330, justify="left").grid(
            row=0, column=0, sticky="ew"
        )

    def _on_consent_change(self) -> None:
        consent = self.consent_var.get()
        self.analytics.set_consent(consent)
        self.start_button.configure(state="normal" if consent else "disabled")

    def _start_session(self) -> None:
        try:
            self.analytics.start_session()
        except ConsentRequiredError as error:
            messagebox.showerror("Consent required", str(error))
            return
        self.status_var.set("Active")
        self.message_var.set(
            "Session active. Aggregate categories are counted only from this field."
        )
        self.practice_text.focus_set()
        self._refresh_metrics()

    def _stop_session(self) -> None:
        self.analytics.stop_session()
        self.status_var.set(self.analytics.state.status)
        self.message_var.set(
            "Session stopped. Aggregates remain visible until deleted or exported."
        )
        self._refresh_metrics()

    def _delete_session(self) -> None:
        self.analytics.delete_current_session()
        self.practice_text.delete("1.0", tk.END)
        self.status_var.set("Idle")
        self.message_var.set(
            "Current in-memory session deleted. Existing exports are not deleted; "
            "remove files manually from data/exports/ when no longer needed."
        )
        self._refresh_metrics()

    def _export_summary(self) -> None:
        summary = self.analytics.summary()
        if not summary.consent_recorded:
            messagebox.showerror(
                "Export unavailable", "Consent is required before exporting a summary."
            )
            return
        if summary.total_events == 0:
            messagebox.showinfo("No events", "There are no aggregate events to export.")
            return
        if self.analytics.state.is_active:
            self.analytics.stop_session()
            self.status_var.set("Stopped")
        json_path, csv_path = self.exporter.export(self.analytics.summary())
        self.message_var.set(f"Exported aggregate summaries locally: {json_path} and {csv_path}")
        self._refresh_metrics()

    def _verify_export(self) -> None:
        path = filedialog.askopenfilename(
            title="Select JSON export to verify",
            initialdir=str(Path("data") / "exports"),
            filetypes=(("JSON files", "*.json"), ("All files", "*.*")),
        )
        if not path:
            return
        verified = verify_json_export(Path(path))
        self.message_var.set(
            "JSON export integrity verified." if verified else "JSON export integrity check failed."
        )

    def _on_key_press(self, event: tk.Event) -> None:
        category = classify_key_event(str(event.keysym), getattr(event, "char", None))
        self.analytics.record_event(category)
        self._refresh_metrics()

    @staticmethod
    def _block_paste(_event: tk.Event) -> str:
        return "break"

    def _refresh_metrics(self) -> None:
        summary = self.analytics.summary()
        self.status_var.set(summary.status)
        self.metric_vars["Duration"].set(f"{summary.duration_seconds} seconds")
        self.metric_vars["Total events"].set(str(summary.total_events))
        self.metric_vars["Backspaces"].set(str(summary.backspace_count))
        self.metric_vars["Pace"].set(f"{summary.typing_pace_events_per_minute} events/min")
        for category, count in summary.counts_by_category.items():
            self.category_vars[category].set(str(count))
        self._draw_chart(summary.counts_by_category)
        if self.analytics.state.is_active:
            self.after(1000, self._refresh_metrics)

    def _draw_chart(self, counts: dict[str, int]) -> None:
        self.canvas.delete("all")
        width = max(self.canvas.winfo_width(), 320)
        max_count = max(counts.values(), default=0) or 1
        bar_height = 14
        gap = 5
        for index, category in enumerate(EVENT_CATEGORIES):
            y = 12 + index * (bar_height + gap)
            bar_width = int((counts[category] / max_count) * (width - 120))
            self.canvas.create_text(4, y + 7, anchor="w", text=category, fill="#222222")
            self.canvas.create_rectangle(
                90, y, 90 + bar_width, y + bar_height, fill="#2f7d6d", outline=""
            )
            self.canvas.create_text(
                width - 12, y + 7, anchor="e", text=str(counts[category]), fill="#222222"
            )
