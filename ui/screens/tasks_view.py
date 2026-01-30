"""Tasks screen: date strip, time grid, task cards, FAB (Phase 2 spec)."""

from datetime import date, timedelta
from typing import Callable, List, Optional

import customtkinter as ctk

from ui.theme import (
    BG_DARK,
    BG_CARD,
    TEXT_PRIMARY,
    TEXT_MUTED,
    ACCENT_MINT_LIGHT,
    CORNER_RADIUS,
    TIMELINE_LABEL_WIDTH,
    FONT_HEADING,
    FONT_BODY,
    FONT_SMALL,
)
from ui.components import TaskCard
from ui.task_dialog import TaskDialog
from models import Task


class TasksView(ctk.CTkFrame):
    """
    Tasks screen: date strip (horizontal days), time grid on left, task cards on right, FAB.
    Connects to TaskPresenter for load/complete/edit/delete/create.
    """

    def __init__(
        self,
        master: ctk.CTk,
        on_new_task: Optional[Callable[[], None]] = None,
        get_presenter=None,
        **kwargs,
    ) -> None:
        super().__init__(master, fg_color=BG_DARK, **kwargs)
        self._on_new_task = on_new_task or (lambda: None)
        self._get_presenter = get_presenter
        self._selected_date = date.today()
        self._day_buttons: list = []
        self._build_ui()

    def _build_ui(self) -> None:
        # Date strip: horizontal day pills
        strip = ctk.CTkScrollableFrame(self, fg_color="transparent", orientation="horizontal")
        strip.pack(fill="x", padx=16, pady=(12, 8))
        self._days_frame = strip
        self._rebuild_days()

        # Content: time labels + scrollable task list
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=16, pady=8)
        left = ctk.CTkFrame(content, fg_color="transparent", width=TIMELINE_LABEL_WIDTH)
        left.pack(side="left", fill="y", padx=(0, 8))
        for hour in range(8, 23):
            label = f"{hour:02d} am" if hour < 12 else f"{hour - 12:02d} pm"
            if hour >= 12 and hour != 12:
                label = f"{hour - 12:02d} pm"
            ctk.CTkLabel(
                left,
                text=label,
                font=FONT_SMALL,
                text_color=TEXT_MUTED,
            ).pack(anchor="w", pady=4)
        self._task_list = ctk.CTkScrollableFrame(
            content,
            fg_color="transparent",
            scrollbar_button_color=BG_CARD,
            scrollbar_button_hover_color=TEXT_MUTED,
        )
        self._task_list.pack(side="left", fill="both", expand=True)

        # FAB
        self._fab = ctk.CTkButton(
            self,
            text="+",
            font=(FONT_BODY[0], 24),
            width=56,
            height=56,
            corner_radius=28,
            fg_color=ACCENT_MINT_LIGHT,
            text_color="#121D2D",
            command=self._on_new_task,
        )
        self._fab.place(relx=1.0, rely=1.0, x=-72, y=-72, anchor="se")

    def _rebuild_days(self) -> None:
        for w in self._days_frame.winfo_children():
            w.destroy()
        self._day_buttons.clear()
        start = self._selected_date - timedelta(days=3)
        for i in range(7):
            d = start + timedelta(days=i)
            is_sel = d == self._selected_date
            btn = ctk.CTkButton(
                self._days_frame,
                text=f"{d.day}\n{d.strftime('%a')}",
                width=56,
                height=56,
                corner_radius=CORNER_RADIUS,
                fg_color=ACCENT_MINT_LIGHT if is_sel else BG_CARD,
                text_color="#121D2D" if is_sel else TEXT_PRIMARY,
                font=FONT_SMALL,
                command=lambda dt=d: self._select_day(dt),
            )
            btn.pack(side="left", padx=4, pady=4)
            self._day_buttons.append((d, btn))

    def _select_day(self, d: date) -> None:
        self._selected_date = d
        self._rebuild_days()
        if self._get_presenter:
            p = self._get_presenter()
            if p and hasattr(p, "load_tasks"):
                p.load_tasks(selected_date=d, search_query=p._last_search or "")

    def get_selected_date(self) -> date:
        return self._selected_date

    def show_tasks(self, tasks: List[Task]) -> None:
        for w in self._task_list.winfo_children():
            w.destroy()
        presenter = self._get_presenter() if self._get_presenter else None
        for task in tasks:
            card = TaskCard(
                self._task_list,
                task=task,
                on_complete=presenter.complete_task if presenter else None,
                on_edit=self._on_edit_task,
                on_delete=presenter.delete_task if presenter else None,
                on_menu=lambda tid: None,
            )
            card.pack(fill="x", pady=4)

    def _on_edit_task(self, task_id: str) -> None:
        presenter = self._get_presenter() if self._get_presenter else None
        if not presenter:
            return
        task = presenter.get_task_by_id(task_id)
        if not task:
            return

        def save_edit(**kwargs) -> None:
            presenter.update_task(
                kwargs["task_id"],
                title=kwargs.get("title"),
                description=kwargs.get("description"),
                due_date=kwargs.get("due_date"),
                duration_minutes=kwargs.get("duration_minutes"),
                priority=kwargs.get("priority"),
            )

        dlg = TaskDialog(self.winfo_toplevel(), dialog_title="Edit Task", on_save=save_edit)
        dlg.set_task(task)
