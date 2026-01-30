"""Calendar screen: month grid (left 70%) + upcoming events sidebar (right 30%)."""

import calendar as cal_module
from datetime import date, datetime, timedelta
from typing import Callable, List, Optional

import customtkinter as ctk

from ui.theme import (
    BG_DARK,
    BG_CARD,
    BG_SIDEBAR,
    TEXT_PRIMARY,
    TEXT_MUTED,
    ACCENT_MINT_LIGHT,
    ACCENT_PURPLE_CAL,
    ACCENT_TEAL,
    ACCENT_BLUE,
    ACCENT_PINK,
    FONT_HEADING,
    FONT_BODY,
    FONT_SMALL,
    FONT_CAPTION,
)
from models import Task


# Card colors for events (match pills)
EVENT_COLORS = [ACCENT_PURPLE_CAL, ACCENT_TEAL, ACCENT_BLUE, ACCENT_PINK, "#FFA500"]


class CalendarView(ctk.CTkFrame):
    """
    Split view: left = month grid (7 columns), right = event list for selected day.
    Background #121D2D. On day click: highlight border #B7E4C7, filter sidebar to that day.
    """

    DAYS_HEADER = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]

    def __init__(
        self,
        master: ctk.CTk,
        get_tasks_for_month: Optional[Callable[[int, int], List[Task]]] = None,
        on_task_click: Optional[Callable[[Task], None]] = None,
        **kwargs,
    ) -> None:
        super().__init__(master, fg_color=BG_DARK, **kwargs)
        self._get_tasks = get_tasks_for_month or (lambda y, m: [])
        self._on_task_click = on_task_click
        self._current = date.today()
        self._selected_day: Optional[date] = None
        self._build_ui()

    def _build_ui(self) -> None:
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=16, pady=16)
        main.columnconfigure(0, weight=7)   # 70% calendar
        main.columnconfigure(1, weight=3)    # 30% sidebar

        # Left: month grid
        left = ctk.CTkFrame(main, fg_color="transparent")
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        left.columnconfigure(0, weight=1)
        # Title + Month/Year toggle
        top = ctk.CTkFrame(left, fg_color="transparent")
        top.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        top.columnconfigure(0, weight=1)
        self._title_label = ctk.CTkLabel(
            top,
            text="",
            font=(FONT_BODY[0], 32),
            text_color=TEXT_PRIMARY,
        )
        self._title_label.grid(row=0, column=0, sticky="w")
        pill = ctk.CTkButton(
            top,
            text="Month",
            font=FONT_SMALL,
            fg_color=ACCENT_PURPLE_CAL,
            text_color=TEXT_PRIMARY,
            corner_radius=20,
            width=80,
            command=lambda: None,
        )
        pill.grid(row=0, column=1)
        # Days of week header
        header_row = ctk.CTkFrame(left, fg_color="transparent")
        header_row.grid(row=1, column=0, sticky="ew", pady=(0, 4))
        for c, day in enumerate(self.DAYS_HEADER):
            cell = ctk.CTkLabel(
                header_row,
                text=day[:3],
                font=FONT_CAPTION,
                text_color=TEXT_MUTED,
            )
            cell.grid(row=0, column=c, padx=2, pady=2, sticky="ew")
            header_row.columnconfigure(c, weight=1)
        # Grid 7 x 6
        self._grid_frame = ctk.CTkFrame(left, fg_color="transparent")
        self._grid_frame.grid(row=2, column=0, sticky="nsew", pady=(0, 8))
        left.rowconfigure(2, weight=1)
        for c in range(7):
            self._grid_frame.columnconfigure(c, weight=1)
        for r in range(6):
            self._grid_frame.rowconfigure(r, weight=1)
        self._day_cells: list = []
        self._fill_grid()

        # Right: event sidebar
        right = ctk.CTkFrame(main, fg_color=BG_SIDEBAR, corner_radius=8)
        right.grid(row=0, column=1, sticky="nsew", padx=(12, 0))
        right.columnconfigure(0, weight=1)
        ctk.CTkLabel(
            right,
            text="Upcoming Events",
            font=FONT_HEADING,
            text_color=TEXT_PRIMARY,
        ).pack(anchor="w", padx=16, pady=(16, 8))
        self._events_list = ctk.CTkScrollableFrame(right, fg_color="transparent")
        self._events_list.pack(fill="both", expand=True, padx=8, pady=8)

    def _fill_grid(self) -> None:
        for w in self._grid_frame.winfo_children():
            w.destroy()
        self._day_cells.clear()
        year, month = self._current.year, self._current.month
        self._title_label.configure(text=f"{cal_module.month_name[month]} {year}")
        cal = cal_module.Calendar(firstweekday=0)  # Monday
        weeks = cal.monthdayscalendar(year, month)
        # Pad to 6 rows
        while len(weeks) < 6:
            weeks.append([0] * 7)
        for r, week in enumerate(weeks[:6]):
            for c, day in enumerate(week):
                cell = ctk.CTkFrame(
                    self._grid_frame,
                    fg_color=BG_CARD,
                    corner_radius=4,
                    border_width=0,
                )
                cell.grid(row=r, column=c, padx=2, pady=2, sticky="nsew")
                if day == 0:
                    lbl = ctk.CTkLabel(cell, text="", font=FONT_SMALL, text_color=TEXT_MUTED)
                else:
                    d = date(year, month, day)
                    is_selected = self._selected_day == d
                    lbl = ctk.CTkLabel(
                        cell,
                        text=str(day),
                        font=FONT_SMALL,
                        text_color=TEXT_PRIMARY if d.month == month else TEXT_MUTED,
                    )
                    if is_selected:
                        cell.configure(border_width=2, border_color=ACCENT_MINT_LIGHT)
                    cell.bind("<Button-1>", lambda e, dt=d: self._on_day_click(dt))
                    lbl.bind("<Button-1>", lambda e, dt=d: self._on_day_click(dt))
                lbl.pack(expand=True)
                self._day_cells.append((cell, day, (year, month, day) if day else None))

    def _on_day_click(self, d: date) -> None:
        self._selected_day = d
        self._fill_grid()
        self._refresh_events()

    def _refresh_events(self) -> None:
        for w in self._events_list.winfo_children():
            w.destroy()
        year, month = self._current.year, self._current.month
        tasks = self._get_tasks(year, month)
        if self._selected_day:
            tasks = [t for t in tasks if t.due_date_time and t.due_date_time.date() == self._selected_day]
        tasks.sort(key=lambda t: (t.due_date_time or datetime.max))
        for i, task in enumerate(tasks[:15]):
            color = EVENT_COLORS[i % len(EVENT_COLORS)]
            card = ctk.CTkFrame(
                self._events_list,
                fg_color=color,
                corner_radius=5,
            )
            card.pack(fill="x", pady=4)
            inner = ctk.CTkFrame(card, fg_color="transparent")
            inner.pack(fill="x", padx=12, pady=10)
            due = task.due_date_time
            day_num = due.day if due else self._selected_day.day if self._selected_day else 0
            ctk.CTkLabel(
                inner,
                text=str(day_num),
                font=(FONT_BODY[0], 24, "bold"),
                text_color=TEXT_PRIMARY,
            ).pack(anchor="w")
            ctk.CTkLabel(
                inner,
                text=task.title.upper(),
                font=FONT_SMALL,
                text_color=TEXT_PRIMARY,
                anchor="w",
            ).pack(fill="x")
            if due:
                ctk.CTkLabel(
                    inner,
                    text=due.strftime("%A, %d %B, %Y"),
                    font=FONT_CAPTION,
                    text_color=TEXT_PRIMARY,
                    anchor="w",
                ).pack(fill="x")
                ctk.CTkLabel(
                    inner,
                    text=due.strftime("%I:%M %p") + " : " + (task.description or task.title),
                    font=FONT_CAPTION,
                    text_color=TEXT_PRIMARY,
                    anchor="w",
                ).pack(fill="x")
            if self._on_task_click:
                card.bind("<Button-1>", lambda e, t=task: self._on_task_click(t))
                inner.bind("<Button-1>", lambda e, t=task: self._on_task_click(t))

    def set_month(self, year: int, month: int) -> None:
        self._current = date(year, month, 1)
        self._fill_grid()
        self._refresh_events()

    def refresh_events(self) -> None:
        """Call when tasks change (e.g. after create/update)."""
        self._fill_grid()
        self._refresh_events()
