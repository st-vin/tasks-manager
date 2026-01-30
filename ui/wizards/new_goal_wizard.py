"""New Goal Wizard: back nav, 3-step progress bar, form (title, description, color)."""

from typing import Callable, Optional

import customtkinter as ctk

from ui.theme import (
    BG_DARK,
    BG_CARD,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    ACCENT_MINT_LIGHT,
    CORNER_RADIUS,
    FONT_HEADING,
    FONT_BODY,
    FONT_SMALL,
)
from models.enums import GoalCategory, FrequencyType


GOAL_COLORS = [
    "#52B788", "#4CAF50", "#2E7D32",  # greens
    "#2196F3", "#1976D2",             # blues
    "#8A2BE2", "#7B1FA2",            # purples
    "#E53935", "#FF5722",             # red/orange
    "#FFC107", "#FFEB3B",            # yellow
]


class NewGoalWizard(ctk.CTkToplevel):
    """
    Modal wizard: Back, title "New Goal", progress bar (3 segments, first active),
    form: Goal Title *, Description, Color (row of circles). On Save calls on_save(title, description, color_hex).
    """

    def __init__(
        self,
        parent: ctk.CTk,
        on_save: Optional[Callable[[str, str, str], None]] = None,
        on_back: Optional[Callable[[], None]] = None,
    ) -> None:
        super().__init__(parent)
        self._on_save = on_save
        self._on_back = on_back
        self._step = 0
        self._selected_color = GOAL_COLORS[0]
        self.title("New Goal")
        self.geometry("440x480")
        self.configure(fg_color=BG_DARK)
        self._build_ui()
        self.transient(parent)
        self.grab_set()
        self._parent = parent

    def _safe_destroy(self) -> None:
        try:
            if self.winfo_exists():
                self.destroy()
        except Exception:
            pass

    def _build_ui(self) -> None:
        # Top nav: back + title
        nav = ctk.CTkFrame(self, fg_color="transparent", height=48)
        nav.pack(fill="x", padx=16, pady=(12, 0))
        nav.pack_propagate(False)
        self._btn_back = ctk.CTkButton(
            nav,
            text="← Back",
            width=80,
            height=40,
            fg_color="transparent",
            hover_color=BG_CARD,
            font=FONT_SMALL,
            command=self._go_back,
        )
        self._btn_back.pack(side="left", padx=(0, 8))
        ctk.CTkLabel(nav, text="New Goal", font=FONT_HEADING, text_color=TEXT_PRIMARY).pack(side="left")

        # Progress bar: 3 segments
        prog = ctk.CTkFrame(self, fg_color="transparent", height=6)
        prog.pack(fill="x", padx=16, pady=(8, 16))
        prog.pack_propagate(False)
        prog.columnconfigure(0, weight=1)
        prog.columnconfigure(1, weight=1)
        prog.columnconfigure(2, weight=1)
        self._seg1 = ctk.CTkFrame(prog, fg_color=ACCENT_MINT_LIGHT, corner_radius=2)
        self._seg1.grid(row=0, column=0, sticky="ew", padx=2)
        self._seg2 = ctk.CTkFrame(prog, fg_color=BG_CARD, corner_radius=2)
        self._seg2.grid(row=0, column=1, sticky="ew", padx=2)
        self._seg3 = ctk.CTkFrame(prog, fg_color=BG_CARD, corner_radius=2)
        self._seg3.grid(row=0, column=2, sticky="ew", padx=2)

        # Form
        form = ctk.CTkFrame(self, fg_color="transparent")
        form.pack(fill="both", expand=True, padx=24, pady=16)
        ctk.CTkLabel(form, text="Goal Title *", font=FONT_BODY, text_color=TEXT_SECONDARY).pack(anchor="w")
        self._title_entry = ctk.CTkEntry(
            form,
            height=40,
            corner_radius=CORNER_RADIUS,
            fg_color=BG_CARD,
            placeholder_text="e.g. Exercise regularly",
            font=FONT_BODY,
            text_color=TEXT_PRIMARY,
        )
        self._title_entry.pack(fill="x", pady=(4, 12))
        ctk.CTkLabel(form, text="Description", font=FONT_BODY, text_color=TEXT_SECONDARY).pack(anchor="w")
        self._desc_entry = ctk.CTkEntry(
            form,
            height=40,
            corner_radius=CORNER_RADIUS,
            fg_color=BG_CARD,
            placeholder_text="Why is this goal important...",
            font=FONT_BODY,
            text_color=TEXT_PRIMARY,
        )
        self._desc_entry.pack(fill="x", pady=(4, 12))
        ctk.CTkLabel(form, text="Color", font=FONT_BODY, text_color=TEXT_SECONDARY).pack(anchor="w", pady=(0, 8))
        color_row = ctk.CTkFrame(form, fg_color="transparent")
        color_row.pack(fill="x", pady=(0, 16))
        self._color_buttons = []
        for c in GOAL_COLORS:
            btn = ctk.CTkButton(
                color_row,
                text="",
                width=32,
                height=32,
                corner_radius=16,
                fg_color=c,
                hover_color=c,
                border_width=2,
                border_color=ACCENT_MINT_LIGHT if c == self._selected_color else "transparent",
                command=lambda col=c: self._pick_color(col),
            )
            btn.pack(side="left", padx=4)
            self._color_buttons.append((c, btn))

        self._btn_save = ctk.CTkButton(
            form,
            text="Save →",
            font=FONT_BODY,
            fg_color=ACCENT_MINT_LIGHT,
            text_color="#121D2D",
            corner_radius=CORNER_RADIUS,
            command=self._save,
        )
        self._btn_save.pack(fill="x", pady=(8, 0))

    def _pick_color(self, color: str) -> None:
        self._selected_color = color
        for c, btn in self._color_buttons:
            btn.configure(border_color=ACCENT_MINT_LIGHT if c == color else "transparent")

    def _go_back(self) -> None:
        if self._on_back:
            self._on_back()
        self.withdraw()
        self.after(200, self._safe_destroy)

    def _save(self) -> None:
        title = self._title_entry.get().strip()
        if not title:
            return
        desc = self._desc_entry.get().strip()
        if self._on_save:
            self._on_save(title, desc, self._selected_color)
        self.withdraw()
        self.after(200, self._safe_destroy)
