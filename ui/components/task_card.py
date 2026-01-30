"""Task card: status, progress, title, description, menu (matching reference image)."""

from typing import Callable, Optional

import customtkinter as ctk

from ui.theme import (
    status_to_color,
    CARD_CORNER_RADIUS,
    FONT_TITLE,
    FONT_BODY,
    FONT_SMALL,
    TEXT_PRIMARY,
    BG_DARK,
)
from models import Task


class TaskCard(ctk.CTkFrame):
    """
    Single task card with status pill, progress bar, title, description, and menu.

    Callbacks: on_complete, on_edit, on_delete, on_menu.
    """

    def __init__(
        self,
        master: ctk.CTk,
        task: Task,
        on_complete: Optional[Callable[[str], None]] = None,
        on_edit: Optional[Callable[[str], None]] = None,
        on_delete: Optional[Callable[[str], None]] = None,
        on_menu: Optional[Callable[[str], None]] = None,
        **kwargs,
    ) -> None:
        super().__init__(master, fg_color="transparent", **kwargs)
        self._task = task
        self._on_complete = on_complete
        self._on_edit = on_edit
        self._on_delete = on_delete
        self._on_menu = on_menu

        status_str = getattr(task.status, "value", str(task.status))
        card_color = status_to_color(status_str)
        # Display label: Completed, Rejected, Running, Upcoming
        display_status = self._status_display_name(status_str)

        inner = ctk.CTkFrame(
            self,
            fg_color=card_color,
            corner_radius=CARD_CORNER_RADIUS,
            border_width=0,
        )
        inner.pack(fill="x", pady=4, padx=0)

        content = ctk.CTkFrame(inner, fg_color="transparent")
        content.pack(fill="x", padx=16, pady=12)

        # Row 1: status pill + (placeholder avatars) + progress + menu
        row1 = ctk.CTkFrame(content, fg_color="transparent")
        row1.pack(fill="x")
        pill = ctk.CTkLabel(
            row1,
            text=display_status,
            font=FONT_SMALL,
            text_color=BG_DARK,
            fg_color=card_color,
            corner_radius=8,
            padx=8,
            pady=2,
        )
        pill.pack(side="left")
        # Placeholder: "avatars" (three circles + plus)
        avatars = ctk.CTkFrame(row1, fg_color="transparent")
        avatars.pack(side="left", padx=(12, 0))
        for _ in range(3):
            ctk.CTkLabel(
                avatars,
                text="",
                width=24,
                height=24,
                fg_color=BG_DARK,
                corner_radius=12,
            ).pack(side="left", padx=2)
        ctk.CTkLabel(
            avatars,
            text="+",
            width=24,
            height=24,
            fg_color=BG_DARK,
            corner_radius=12,
            text_color=card_color,
            font=FONT_BODY,
        ).pack(side="left", padx=2)
        # Progress
        prog_frame = ctk.CTkFrame(row1, fg_color="transparent")
        prog_frame.pack(side="left", expand=True, fill="x", padx=8)
        pct = getattr(task, "progress_percent", 0) or (100 if task.is_completed else 0)
        ctk.CTkProgressBar(
            prog_frame,
            width=80,
            height=6,
            progress_color=BG_DARK,
            fg_color="white",
            corner_radius=3,
            progress=pct / 100.0,
        ).pack(side="left")
        ctk.CTkLabel(
            prog_frame,
            text=f"{pct}%",
            font=FONT_SMALL,
            text_color=BG_DARK,
        ).pack(side="left", padx=4)
        # Menu button
        menu_btn = ctk.CTkButton(
            row1,
            text="⋮",
            width=32,
            height=32,
            fg_color="transparent",
            hover_color=BG_DARK,
            text_color=BG_DARK,
            font=FONT_BODY,
            command=self._on_menu_click,
        )
        menu_btn.pack(side="right")

        # Row 2: icon placeholder + title + description
        row2 = ctk.CTkFrame(content, fg_color="transparent")
        row2.pack(fill="x", pady=(8, 0))
        icon = ctk.CTkLabel(
            row2,
            text="▣",
            width=40,
            height=40,
            fg_color=BG_DARK,
            corner_radius=8,
            text_color=card_color,
            font=FONT_BODY,
        )
        icon.pack(side="left")
        titles = ctk.CTkFrame(row2, fg_color="transparent")
        titles.pack(side="left", fill="x", expand=True, padx=12)
        ctk.CTkLabel(
            titles,
            text=task.title,
            font=FONT_TITLE,
            text_color=BG_DARK,
            anchor="w",
        ).pack(fill="x")
        if task.description:
            ctk.CTkLabel(
                titles,
                text=task.description,
                font=FONT_SMALL,
                text_color=BG_DARK,
                anchor="w",
            ).pack(fill="x")

    def _status_display_name(self, status: str) -> str:
        """Map internal status to UI label."""
        s = status.lower()
        if "completed" in s:
            return "Completed"
        if "cancelled" in s or "rejected" in s:
            return "Rejected"
        if "in_progress" in s or "running" in s:
            return "Running"
        if "upcoming" in s or "today" in s or "pending" in s or "scheduled" in s:
            return "Upcoming"
        if "overdue" in s:
            return "Overdue"
        return "Task"

    def _on_menu_click(self) -> None:
        if self._on_menu:
            self._on_menu(self._task.task_id)
        # Optional: show popup with Edit / Delete / Complete
        if self._on_edit or self._on_delete or self._on_complete:
            self._show_context_menu()

    def _show_context_menu(self) -> None:
        """Show simple context menu (Edit, Delete, Complete)."""
        menu = ctk.CTkToplevel(self)
        menu.wm_overrideredirect(True)
        menu.wm_geometry(f"+{self.winfo_rootx() + 200}+{self.winfo_rooty() + 50}")
        f = ctk.CTkFrame(menu, fg_color=BG_DARK, corner_radius=8)
        f.pack(padx=2, pady=2)
        if self._on_complete and not self._task.is_completed:
            ctk.CTkButton(
                f,
                text="Mark complete",
                command=lambda: (self._on_complete(self._task.task_id), menu.destroy()),
                fg_color="transparent",
                width=140,
            ).pack(pady=2, padx=4)
        if self._on_edit:
            ctk.CTkButton(
                f,
                text="Edit",
                command=lambda: (self._on_edit(self._task.task_id), menu.destroy()),
                fg_color="transparent",
                width=140,
            ).pack(pady=2, padx=4)
        if self._on_delete:
            ctk.CTkButton(
                f,
                text="Delete",
                command=lambda: (self._on_delete(self._task.task_id), menu.destroy()),
                fg_color="transparent",
                width=140,
            ).pack(pady=2, padx=4)
        def close(_=None):
            menu.destroy()
        menu.bind("<FocusOut>", close)
        menu.after(200, menu.focus_set)
