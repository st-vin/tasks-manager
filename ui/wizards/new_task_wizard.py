"""New Task Wizard: step 1 = task type selection (Free Task, Goal Task, Assignment)."""

from typing import Callable, Optional

import customtkinter as ctk

from ui.theme import (
    BG_DARK,
    BG_CARD,
    TEXT_PRIMARY,
    TEXT_MUTED,
    ACCENT_MINT_LIGHT,
    ACCENT_TASK_CARD,
    CORNER_RADIUS,
    FONT_HEADING,
    FONT_BODY,
    FONT_SMALL,
)
from models.enums import TaskType


class NewTaskWizard(ctk.CTkToplevel):
    """
    Step 1: Back, "New Task", progress bar (first segment active).
    List: "What type of task?" with options Free Task (selected), Goal Task, Assignment.
    Selected = light green bg, checkmark. On select Free Task and "Next" (or open details),
    call on_select_type(TaskType) then optionally open TaskDialog for details.
    """

    def __init__(
        self,
        parent: ctk.CTk,
        on_select_type: Optional[Callable[[TaskType], None]] = None,
        on_back: Optional[Callable[[], None]] = None,
    ) -> None:
        super().__init__(parent)
        self._on_select_type = on_select_type
        self._on_back = on_back
        self._selected: TaskType = TaskType.FREE
        self.title("New Task")
        self.geometry("420x400")
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
        ctk.CTkLabel(nav, text="New Task", font=FONT_HEADING, text_color=TEXT_PRIMARY).pack(side="left")

        prog = ctk.CTkFrame(self, fg_color="transparent", height=6)
        prog.pack(fill="x", padx=16, pady=(8, 16))
        prog.pack_propagate(False)
        self._seg1 = ctk.CTkFrame(prog, fg_color=ACCENT_MINT_LIGHT, corner_radius=2, height=6)
        self._seg1.pack(fill="x", side="left", expand=True, padx=2)
        self._seg2 = ctk.CTkFrame(prog, fg_color=BG_CARD, corner_radius=2, height=6)
        self._seg2.pack(fill="x", side="left", expand=True, padx=2)
        self._seg3 = ctk.CTkFrame(prog, fg_color=BG_CARD, corner_radius=2, height=6)
        self._seg3.pack(fill="x", side="left", expand=True, padx=2)

        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=24, pady=16)
        ctk.CTkLabel(
            content,
            text="What type of task?",
            font=FONT_BODY,
            text_color=TEXT_PRIMARY,
        ).pack(anchor="w", pady=(0, 12))

        options = [
            (TaskType.FREE, "📄", "Free Task"),
            (TaskType.GOAL, "🎯", "Goal Task"),
            (TaskType.ASSIGNMENT, "📚", "Assignment"),
        ]
        self._option_frames = []
        for typ, icon, label in options:
            is_sel = typ == self._selected
            frame = ctk.CTkFrame(
                content,
                fg_color=ACCENT_TASK_CARD if is_sel else "transparent",
                corner_radius=CORNER_RADIUS,
                border_width=0,
            )
            frame.pack(fill="x", pady=4)
            row = ctk.CTkFrame(frame, fg_color="transparent")
            row.pack(fill="x", padx=16, pady=12)
            ctk.CTkLabel(
                row,
                text=icon,
                font=FONT_BODY,
                width=32,
                height=32,
                fg_color=BG_CARD,
                corner_radius=8,
            ).pack(side="left", padx=(0, 12))
            ctk.CTkLabel(
                row,
                text=label,
                font=FONT_BODY,
                text_color="#121D2D" if is_sel else TEXT_PRIMARY,
                anchor="w",
            ).pack(side="left", fill="x", expand=True)
            if is_sel:
                ctk.CTkLabel(row, text="✓", font=FONT_BODY, text_color="#121D2D").pack(side="right")
            frame.bind("<Button-1>", lambda e, t=typ: self._select(t))
            row.bind("<Button-1>", lambda e, t=typ: self._select(t))
            self._option_frames.append((typ, frame, row))
            frame.configure(cursor="hand2")
            row.configure(cursor="hand2")

        self._btn_next = ctk.CTkButton(
            content,
            text="Next →",
            font=FONT_BODY,
            fg_color=ACCENT_MINT_LIGHT,
            text_color="#121D2D",
            corner_radius=CORNER_RADIUS,
            command=self._next,
        )
        self._btn_next.pack(fill="x", pady=(20, 0))

    def _select(self, typ: TaskType) -> None:
        self._selected = typ
        for t, frame, row in self._option_frames:
            frame.configure(fg_color=ACCENT_TASK_CARD if t == typ else "transparent")
            for child in row.winfo_children():
                if isinstance(child, ctk.CTkLabel) and child.cget("text") == "✓":
                    child.destroy()
                    break
            if t == typ:
                ctk.CTkLabel(row, text="✓", font=FONT_BODY, text_color="#121D2D").pack(side="right")
                for lbl in row.winfo_children():
                    if isinstance(lbl, ctk.CTkLabel) and lbl.cget("text") not in ("✓",):
                        lbl.configure(text_color="#121D2D")
                break
        for t, frame, row in self._option_frames:
            if t != typ:
                for lbl in row.winfo_children():
                    if isinstance(lbl, ctk.CTkLabel) and lbl.cget("text") not in ("✓",) and "Task" in lbl.cget("text"):
                        lbl.configure(text_color=TEXT_PRIMARY)

    def _go_back(self) -> None:
        if self._on_back:
            self._on_back()
        self.withdraw()
        self.after(200, self._safe_destroy)

    def _next(self) -> None:
        sel = self._selected
        cb = self._on_select_type
        if cb:
            cb(sel)
        self.withdraw()
        self.after(200, self._safe_destroy)
