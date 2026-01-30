"""Goals Page: banner, Active/Archived tab, list, empty state, FAB (Phase 2 spec)."""

from typing import Callable, List, Optional

import customtkinter as ctk

from ui.theme import (
    BG_DARK,
    BG_CARD,
    TEXT_PRIMARY,
    TEXT_MUTED,
    ACCENT_PURPLE,
    ACCENT_MINT_LIGHT,
    CORNER_RADIUS,
    FONT_HEADING,
    FONT_BODY,
    FONT_SMALL,
)
from models import Goal


class GoalsView(ctk.CTkFrame):
    """
    Goals screen: purple header banner (Active Goals | 0, Total Streaks | 0),
    pill tab (Active / Archived), list or empty state, FAB + Create Goal button.
    """

    def __init__(
        self,
        master: ctk.CTk,
        on_create_goal: Optional[Callable[[], None]] = None,
        on_back: Optional[Callable[[], None]] = None,
        **kwargs,
    ) -> None:
        super().__init__(master, fg_color=BG_DARK, **kwargs)
        self._on_create_goal = on_create_goal or (lambda: None)
        self._on_back = on_back
        self._show_active = True
        self._build_ui()

    def _build_ui(self) -> None:
        # Header banner: full-width, corner_radius=15 (bottom), purple
        banner = ctk.CTkFrame(self, fg_color=ACCENT_PURPLE, corner_radius=15, height=80)
        banner.pack(fill="x", padx=16, pady=(16, 12))
        banner.pack_propagate(False)
        inner = ctk.CTkFrame(banner, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=20, pady=12)
        inner.columnconfigure(0, weight=1)
        inner.columnconfigure(1, weight=1)
        self._active_label = ctk.CTkLabel(
            inner,
            text="Active Goals | 0",
            font=FONT_HEADING,
            text_color=TEXT_PRIMARY,
        )
        self._active_label.grid(row=0, column=0, sticky="w")
        self._streaks_label = ctk.CTkLabel(
            inner,
            text="Total Streaks | 0",
            font=FONT_HEADING,
            text_color=TEXT_PRIMARY,
        )
        self._streaks_label.grid(row=0, column=1, sticky="e")

        # Tab switcher: Active (0) / Archived (0)
        tab_frame = ctk.CTkFrame(self, fg_color="transparent")
        tab_frame.pack(fill="x", padx=16, pady=8)
        self._btn_active = ctk.CTkButton(
            tab_frame,
            text="Active (0)",
            font=FONT_SMALL,
            fg_color=ACCENT_MINT_LIGHT,
            text_color="#121D2D",
            corner_radius=20,
            height=36,
            width=100,
            command=lambda: self._switch_tab(True),
        )
        self._btn_active.pack(side="left", padx=(0, 8))
        self._btn_archived = ctk.CTkButton(
            tab_frame,
            text="Archived (0)",
            font=FONT_SMALL,
            fg_color="transparent",
            text_color=TEXT_MUTED,
            corner_radius=20,
            height=36,
            width=100,
            command=lambda: self._switch_tab(False),
        )
        self._btn_archived.pack(side="left")

        # Content: list or empty state
        self._content = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self._content.pack(fill="both", expand=True, padx=16, pady=8)

        # Empty state (center)
        self._empty_frame = ctk.CTkFrame(self._content, fg_color="transparent")
        self._empty_frame.pack(expand=True, pady=40)
        ctk.CTkLabel(
            self._empty_frame,
            text="🎯",
            font=(FONT_BODY[0], 48),
            text_color=TEXT_MUTED,
        ).pack(pady=(0, 8))
        ctk.CTkLabel(
            self._empty_frame,
            text="No goals yet",
            font=FONT_HEADING,
            text_color=TEXT_PRIMARY,
        ).pack(pady=4)
        ctk.CTkLabel(
            self._empty_frame,
            text="Create your first goal...",
            font=FONT_BODY,
            text_color=TEXT_MUTED,
        ).pack(pady=(0, 16))
        ctk.CTkButton(
            self._empty_frame,
            text="Create Goal",
            font=FONT_BODY,
            fg_color=ACCENT_MINT_LIGHT,
            text_color="#121D2D",
            corner_radius=CORNER_RADIUS,
            command=self._on_create_goal,
        ).pack(pady=4)

        # FAB bottom right
        self._fab = ctk.CTkButton(
            self,
            text="+",
            font=(FONT_BODY[0], 24),
            width=56,
            height=56,
            corner_radius=28,
            fg_color=ACCENT_MINT_LIGHT,
            text_color="#121D2D",
            command=self._on_create_goal,
        )
        self._fab.place(relx=1.0, rely=1.0, x=-72, y=-72, anchor="se")

    def _switch_tab(self, active: bool) -> None:
        self._show_active = active
        self._btn_active.configure(
            fg_color=ACCENT_MINT_LIGHT if active else "transparent",
            text_color="#121D2D" if active else TEXT_MUTED,
        )
        self._btn_archived.configure(
            fg_color=ACCENT_MINT_LIGHT if not active else "transparent",
            text_color="#121D2D" if not active else TEXT_MUTED,
        )
        if hasattr(self, "_on_tab_changed") and self._on_tab_changed:
            self._on_tab_changed(active)

    def set_tab_callback(self, callback: Callable[[bool], None]) -> None:
        self._on_tab_changed = callback

    def set_banner_counts(self, active_count: int, total_streaks: int) -> None:
        self._active_label.configure(text=f"Active Goals | {active_count}")
        self._streaks_label.configure(text=f"Total Streaks | {total_streaks}")

    def set_tab_labels(self, active_count: int, archived_count: int) -> None:
        self._btn_active.configure(text=f"Active ({active_count})")
        self._btn_archived.configure(text=f"Archived ({archived_count})")

    def show_goals(self, goals: List[Goal], active: bool) -> None:
        """Show goal list or empty state."""
        for w in self._content.winfo_children():
            w.destroy()
        if not goals:
            empty = ctk.CTkFrame(self._content, fg_color="transparent")
            empty.pack(expand=True, pady=40)
            ctk.CTkLabel(empty, text="🎯", font=(FONT_BODY[0], 48), text_color=TEXT_MUTED).pack(pady=(0, 8))
            ctk.CTkLabel(empty, text="No goals yet", font=FONT_HEADING, text_color=TEXT_PRIMARY).pack(pady=4)
            ctk.CTkLabel(empty, text="Create your first goal...", font=FONT_BODY, text_color=TEXT_MUTED).pack(pady=(0, 16))
            ctk.CTkButton(
                empty,
                text="Create Goal",
                font=FONT_BODY,
                fg_color=ACCENT_MINT_LIGHT,
                text_color="#121D2D",
                corner_radius=CORNER_RADIUS,
                command=self._on_create_goal,
            ).pack(pady=4)
        else:
            for goal in goals:
                card = ctk.CTkFrame(self._content, fg_color=BG_CARD, corner_radius=CORNER_RADIUS)
                card.pack(fill="x", pady=4)
                row = ctk.CTkFrame(card, fg_color="transparent")
                row.pack(fill="x", padx=16, pady=12)
                color_dot = ctk.CTkLabel(
                    row,
                    text="",
                    width=12,
                    height=12,
                    fg_color=goal.color_hex or "#4CAF50",
                    corner_radius=6,
                )
                color_dot.pack(side="left", padx=(0, 12))
                ctk.CTkLabel(row, text=goal.title, font=FONT_BODY, text_color=TEXT_PRIMARY, anchor="w").pack(side="left", fill="x", expand=True)
                ctk.CTkLabel(row, text=f"Streak: {goal.current_streak}", font=FONT_SMALL, text_color=TEXT_MUTED).pack(side="right")
