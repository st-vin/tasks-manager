"""Home Dashboard: greeting, KPI cards, upcoming tasks, quick actions (Phase 2 spec)."""

from datetime import datetime
from typing import Callable, List, Optional

import customtkinter as ctk

from ui.theme import (
    BG_DARK,
    BG_CARD,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    TEXT_MUTED,
    ACCENT_MINT_LIGHT,
    ACCENT_MINT,
    ACCENT_ORANGE,
    ACCENT_ORANGE_DARK,
    CORNER_RADIUS,
    FONT_HEADING_LARGE,
    FONT_HEADING,
    FONT_BODY,
    FONT_SMALL,
    FONT_FAMILY,
)
from models import Task


class HomeDashboardView(ctk.CTkScrollableFrame):
    """
    Home screen: header (date + greeting), two KPI cards (completion rate, streaks),
    upcoming tasks list, quick actions (New Task, New Goal).
    """

    def __init__(
        self,
        master: ctk.CTk,
        on_new_task: Optional[Callable[[], None]] = None,
        on_new_goal: Optional[Callable[[], None]] = None,
        on_view_all_tasks: Optional[Callable[[], None]] = None,
        **kwargs,
    ) -> None:
        super().__init__(master, fg_color=BG_DARK, **kwargs)
        self._on_new_task = on_new_task
        self._on_new_goal = on_new_goal
        self._on_view_all = on_view_all_tasks
        self._build_ui()

    def _build_ui(self) -> None:
        # Header: date (small grey) + greeting (bold white 24px)
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=16, pady=(16, 8))
        date_str = datetime.now().strftime("%A, %b %d")
        ctk.CTkLabel(
            header,
            text=date_str,
            font=FONT_SMALL,
            text_color=TEXT_MUTED,
        ).pack(anchor="w")
        self._greeting_label = ctk.CTkLabel(
            header,
            text="Good evening, User!",
            font=FONT_HEADING_LARGE,
            text_color=TEXT_PRIMARY,
        )
        self._greeting_label.pack(anchor="w")

        # KPI cards row (two cards)
        kpi_frame = ctk.CTkFrame(self, fg_color="transparent")
        kpi_frame.pack(fill="x", padx=16, pady=12)
        kpi_frame.columnconfigure(0, weight=1)
        kpi_frame.columnconfigure(1, weight=1)
        self._card_completion = self._make_kpi_card(
            kpi_frame,
            icon_text="✓",
            value_key="completion",
            label="Completion Rate",
            top_color=ACCENT_MINT_LIGHT,
            bottom_color=ACCENT_MINT,
            row=0,
            col=0,
        )
        self._card_streaks = self._make_kpi_card(
            kpi_frame,
            icon_text="🔥",
            value_key="streaks",
            label="Active Streaks",
            top_color=ACCENT_ORANGE,
            bottom_color=ACCENT_ORANGE_DARK,
            row=0,
            col=1,
        )

        # Upcoming Tasks section
        upcoming_frame = ctk.CTkFrame(self, fg_color="transparent")
        upcoming_frame.pack(fill="x", padx=16, pady=16)
        row1 = ctk.CTkFrame(upcoming_frame, fg_color="transparent")
        row1.pack(fill="x")
        ctk.CTkLabel(
            row1,
            text="🕐  Upcoming Tasks",
            font=FONT_HEADING,
            text_color=TEXT_PRIMARY,
        ).pack(side="left")
        view_all_btn = ctk.CTkButton(
            row1,
            text="View all >",
            font=FONT_SMALL,
            fg_color="transparent",
            hover_color=BG_CARD,
            text_color=TEXT_SECONDARY,
            command=self._on_view_all or (lambda: None),
        )
        view_all_btn.pack(side="right")
        self._upcoming_list = ctk.CTkFrame(upcoming_frame, fg_color="transparent")
        self._upcoming_list.pack(fill="x", pady=(8, 0))

        # Quick Actions
        actions_frame = ctk.CTkFrame(self, fg_color="transparent")
        actions_frame.pack(fill="x", padx=16, pady=8)
        actions_frame.columnconfigure(0, weight=1)
        actions_frame.columnconfigure(1, weight=1)
        self._btn_new_task = ctk.CTkButton(
            actions_frame,
            text="",
            font=FONT_BODY,
            fg_color=BG_CARD,
            hover_color=ACCENT_MINT_LIGHT,
            corner_radius=CORNER_RADIUS,
            height=56,
            anchor="w",
            command=self._on_new_task or (lambda: None),
        )
        self._btn_new_task.grid(row=0, column=0, padx=(0, 6), pady=4, sticky="ew")
        self._build_quick_action(self._btn_new_task, "📊", "New Task", "Create a task")
        self._btn_new_goal = ctk.CTkButton(
            actions_frame,
            text="",
            font=FONT_BODY,
            fg_color=BG_CARD,
            hover_color=ACCENT_MINT_LIGHT,
            corner_radius=CORNER_RADIUS,
            height=56,
            anchor="w",
            command=self._on_new_goal or (lambda: None),
        )
        self._btn_new_goal.grid(row=0, column=1, padx=(6, 0), pady=4, sticky="ew")
        self._build_quick_action(self._btn_new_goal, "🎯", "New Goal", "Create a goal")

    def _build_quick_action(self, parent: ctk.CTkButton, icon: str, title: str, subtitle: str) -> None:
        # Custom content inside button: icon (dark circle), title (bold), subtitle (grey)
        # Use a single inner frame so clicks anywhere trigger the button's command
        cmd = parent.cget("command") or (lambda: None)
        inner = ctk.CTkFrame(parent, fg_color="transparent", cursor="hand2")
        inner.place(relx=0.03, rely=0.1, relwidth=0.94, relheight=0.8)
        inner.bind("<Button-1>", lambda e: cmd())
        icon_lbl = ctk.CTkLabel(
            inner,
            text=icon,
            width=36,
            height=36,
            fg_color=BG_DARK,
            corner_radius=18,
            font=FONT_BODY,
            cursor="hand2",
        )
        icon_lbl.pack(side="left", padx=(0, 12))
        icon_lbl.bind("<Button-1>", lambda e: cmd())
        texts = ctk.CTkFrame(inner, fg_color="transparent", cursor="hand2")
        texts.pack(side="left", fill="x", expand=True)
        texts.bind("<Button-1>", lambda e: cmd())
        t1 = ctk.CTkLabel(texts, text=title, font=FONT_HEADING, text_color=TEXT_PRIMARY, anchor="w", cursor="hand2")
        t1.pack(fill="x")
        t1.bind("<Button-1>", lambda e: cmd())
        t2 = ctk.CTkLabel(texts, text=subtitle, font=FONT_SMALL, text_color=TEXT_MUTED, anchor="w", cursor="hand2")
        t2.pack(fill="x")
        t2.bind("<Button-1>", lambda e: cmd())

    def _make_kpi_card(
        self,
        parent: ctk.CTkFrame,
        icon_text: str,
        value_key: str,
        label: str,
        top_color: str,
        bottom_color: str,
        row: int,
        col: int,
    ) -> ctk.CTkFrame:
        card_w, card_h = 200, 100
        card = ctk.CTkFrame(parent, fg_color=top_color, corner_radius=CORNER_RADIUS, width=card_w, height=card_h)
        card.pack_propagate(False)
        card.grid(row=row, column=col, padx=6, pady=6, sticky="nsew")
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)
        ctk.CTkLabel(content, text=icon_text, font=(FONT_FAMILY, 20), text_color="#121D2D").pack(anchor="w")
        value_lbl = ctk.CTkLabel(content, text="0", font=(FONT_FAMILY, 28, "bold"), text_color="#121D2D")
        value_lbl.pack(anchor="w")
        if value_key == "completion":
            self._completion_value_label = value_lbl
        else:
            self._streaks_value_label = value_lbl
        ctk.CTkLabel(content, text=label, font=FONT_SMALL, text_color="#121D2D").pack(anchor="w")
        return card

    def set_greeting(self, text: str) -> None:
        self._greeting_label.configure(text=text)

    def set_user_name(self, name: str) -> None:
        hour = datetime.now().hour
        if hour < 12:
            greeting = "Good morning"
        elif hour < 17:
            greeting = "Good afternoon"
        else:
            greeting = "Good evening"
        self._greeting_label.configure(text=f"{greeting}, {name}!")

    def set_completion_rate(self, pct: int) -> None:
        if hasattr(self, "_completion_value_label"):
            self._completion_value_label.configure(text=f"{pct}%")

    def set_active_streaks(self, count: int) -> None:
        if hasattr(self, "_streaks_value_label"):
            self._streaks_value_label.configure(text=str(count))

    def set_upcoming_tasks(self, tasks: List[Task]) -> None:
        for w in self._upcoming_list.winfo_children():
            w.destroy()
        if not tasks:
            ctk.CTkLabel(
                self._upcoming_list,
                text="No upcoming tasks",
                font=FONT_BODY,
                text_color=TEXT_MUTED,
            ).pack(pady=20)
        else:
            for task in tasks[:5]:
                due = ""
                if task.due_date_time:
                    due = task.due_date_time.strftime("%b %d, %H:%M")
                ctk.CTkLabel(
                    self._upcoming_list,
                    text=f"{task.title}" + (f" — {due}" if due else ""),
                    font=FONT_SMALL,
                    text_color=TEXT_PRIMARY,
                    anchor="w",
                ).pack(fill="x", pady=2)

    def refresh(
        self,
        user_name: str,
        completion_pct: int,
        active_streaks: int,
        upcoming_tasks: List[Task],
    ) -> None:
        self.set_user_name(user_name)
        self.set_completion_rate(completion_pct)
        self.set_active_streaks(active_streaks)
        self.set_upcoming_tasks(upcoming_tasks)
