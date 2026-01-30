"""Create/Edit Task dialog."""

from datetime import datetime
from typing import Any, Callable, Optional

import customtkinter as ctk

from ui.theme import BG_DARK, BG_INPUT, TEXT_PRIMARY, TEXT_SECONDARY, CORNER_RADIUS, FONT_BODY
from models import Task
from models.enums import Priority


class TaskDialog(ctk.CTkToplevel):
    """
    Modal dialog to create or edit a task.
    On OK calls on_save(**kwargs). For create: title, description, due_date, duration_minutes, priority.
    For edit: task_id, title, description, due_date, duration_minutes, priority.
    """

    def __init__(self, parent: ctk.CTk, dialog_title: str = "New Task", on_save: Optional[Callable[..., None]] = None):
        super().__init__(parent)
        self._on_save = on_save
        self._task: Optional[Task] = None
        self.title(dialog_title)
        self.geometry("420x380")
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
        f = ctk.CTkFrame(self, fg_color="transparent")
        f.pack(fill="both", expand=True, padx=24, pady=24)
        ctk.CTkLabel(f, text="Title", font=FONT_BODY, text_color=TEXT_SECONDARY).pack(anchor="w")
        self._title_entry = ctk.CTkEntry(
            f,
            height=40,
            corner_radius=CORNER_RADIUS,
            fg_color=BG_INPUT,
            text_color=TEXT_PRIMARY,
            font=FONT_BODY,
            placeholder_text="Task title",
        )
        self._title_entry.pack(fill="x", pady=(4, 12))
        ctk.CTkLabel(f, text="Description", font=FONT_BODY, text_color=TEXT_SECONDARY).pack(anchor="w")
        self._desc_entry = ctk.CTkEntry(
            f,
            height=40,
            corner_radius=CORNER_RADIUS,
            fg_color=BG_INPUT,
            text_color=TEXT_PRIMARY,
            font=FONT_BODY,
            placeholder_text="Description (optional)",
        )
        self._desc_entry.pack(fill="x", pady=(4, 12))
        ctk.CTkLabel(f, text="Due date & time (optional)", font=FONT_BODY, text_color=TEXT_SECONDARY).pack(anchor="w")
        self._due_entry = ctk.CTkEntry(
            f,
            height=40,
            corner_radius=CORNER_RADIUS,
            fg_color=BG_INPUT,
            text_color=TEXT_PRIMARY,
            font=FONT_BODY,
            placeholder_text="YYYY-MM-DD HH:MM or leave empty",
        )
        self._due_entry.pack(fill="x", pady=(4, 12))
        ctk.CTkLabel(f, text="Duration (minutes)", font=FONT_BODY, text_color=TEXT_SECONDARY).pack(anchor="w")
        self._duration_entry = ctk.CTkEntry(
            f,
            height=40,
            corner_radius=CORNER_RADIUS,
            fg_color=BG_INPUT,
            text_color=TEXT_PRIMARY,
            font=FONT_BODY,
            placeholder_text="0",
        )
        self._duration_entry.pack(fill="x", pady=(4, 12))
        ctk.CTkLabel(f, text="Priority", font=FONT_BODY, text_color=TEXT_SECONDARY).pack(anchor="w")
        self._priority_combo = ctk.CTkComboBox(
            f,
            values=[p.value for p in Priority],
            height=40,
            corner_radius=CORNER_RADIUS,
            fg_color=BG_INPUT,
            button_color=BG_INPUT,
            button_hover_color=BG_INPUT,
        )
        self._priority_combo.pack(fill="x", pady=(4, 16))
        btn_row = ctk.CTkFrame(f, fg_color="transparent")
        btn_row.pack(fill="x")
        ctk.CTkButton(
            btn_row,
            text="← Cancel",
            fg_color=BG_INPUT,
            hover_color=TEXT_SECONDARY,
            command=lambda: (self.withdraw(), self.after(200, self._safe_destroy)),
        ).pack(side="right", padx=8)
        ctk.CTkButton(btn_row, text="Save →", command=self._save).pack(side="right")

    def set_task(self, task: Task) -> None:
        """Pre-fill form for editing."""
        self._task = task
        self._title_entry.delete(0, "end")
        self._title_entry.insert(0, task.title)
        self._desc_entry.delete(0, "end")
        self._desc_entry.insert(0, task.description or "")
        self._due_entry.delete(0, "end")
        if task.due_date_time:
            self._due_entry.insert(0, task.due_date_time.strftime("%Y-%m-%d %H:%M"))
        self._duration_entry.delete(0, "end")
        self._duration_entry.insert(0, str(task.duration_minutes or 0))
        self._priority_combo.set(getattr(task.priority, "value", str(task.priority)))

    def _parse_due(self) -> Optional[datetime]:
        s = self._due_entry.get().strip()
        if not s:
            return None
        try:
            return datetime.strptime(s, "%Y-%m-%d %H:%M")
        except ValueError:
            try:
                return datetime.strptime(s, "%Y-%m-%d")
            except ValueError:
                return None

    def _parse_duration(self) -> int:
        try:
            return max(0, int(self._duration_entry.get().strip() or "0"))
        except ValueError:
            return 0

    def _save(self) -> None:
        title = self._title_entry.get().strip()
        if not title:
            return
        desc = self._desc_entry.get().strip()
        due = self._parse_due()
        duration = self._parse_duration()
        try:
            prio = Priority(self._priority_combo.get())
        except ValueError:
            prio = Priority.MEDIUM
        if self._on_save:
            if self._task:
                self._on_save(
                    task_id=self._task.task_id,
                    title=title,
                    description=desc,
                    due_date=due,
                    duration_minutes=duration,
                    priority=prio,
                )
            else:
                self._on_save(
                    title=title,
                    description=desc,
                    due_date=due,
                    duration_minutes=duration,
                    priority=prio,
                )
        self.withdraw()
        self.after(200, self._safe_destroy)
