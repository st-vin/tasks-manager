"""Date selector: month/year display + day carousel (pill-shaped)."""

from datetime import date, datetime, timedelta
from typing import Callable, Optional

import customtkinter as ctk

from ui.theme import (
    BG_CARD,
    BG_INPUT,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    STATUS_COMPLETED,
    CORNER_RADIUS,
    FONT_HEADING,
    FONT_BODY,
    FONT_SMALL,
)


class DateSelector(ctk.CTkFrame):
    """
    Month/year label with chevron + horizontal scroll of day pills.

    Selected day is highlighted (green). Calls on_date_selected(date) when user picks a day.
    """

    def __init__(
        self,
        master: ctk.CTk,
        initial_date: Optional[date] = None,
        on_date_selected: Optional[Callable[[date], None]] = None,
        **kwargs,
    ) -> None:
        super().__init__(master, fg_color="transparent", **kwargs)
        self._selected: date = initial_date or date.today()
        self._on_date_selected = on_date_selected
        self._day_buttons: list[tuple[datetime, ctk.CTkButton]] = []

        # Month/Year row
        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", pady=(0, 8))
        self._month_label = ctk.CTkLabel(
            top,
            text=self._format_month_year(self._selected),
            font=FONT_HEADING,
            text_color=TEXT_PRIMARY,
        )
        self._month_label.pack(side="left")
        chevron = ctk.CTkLabel(
            top,
            text=" ⌄",
            font=FONT_HEADING,
            text_color=TEXT_SECONDARY,
        )
        chevron.pack(side="left", padx=(4, 0))
        # Optional: bind chevron to open month picker; for now we only use day carousel

        # Day carousel (scrollable frame with pills)
        self._days_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            orientation="horizontal",
            scrollbar_button_color=BG_CARD,
            scrollbar_button_hover_color=BG_INPUT,
        )
        self._days_frame.pack(fill="x", pady=0)
        self._build_day_pills()

    def _format_month_year(self, d: date) -> str:
        return d.strftime("%B %Y")

    def _build_day_pills(self) -> None:
        for w in self._days_frame.winfo_children():
            w.destroy()
        self._day_buttons.clear()
        start = self._selected - timedelta(days=7)
        for i in range(15):
            d = start + timedelta(days=i)
            btn = ctk.CTkButton(
                self._days_frame,
                text=f"{d.day}\n{d.strftime('%a')}",
                width=70,
                height=56,
                corner_radius=CORNER_RADIUS,
                fg_color=STATUS_COMPLETED if self._is_selected(d) else BG_CARD,
                text_color="#1a1d29" if self._is_selected(d) else TEXT_PRIMARY,
                hover_color=BG_INPUT if not self._is_selected(d) else STATUS_COMPLETED,
                font=FONT_SMALL,
                command=lambda dt=d: self._select_day(dt),
            )
            btn.pack(side="left", padx=4, pady=4)
            self._day_buttons.append((d, btn))
        self._month_label.configure(text=self._format_month_year(self._selected))

    def _is_selected(self, d: date) -> bool:
        return d == self._selected

    def _select_day(self, d: date) -> None:
        self._selected = d
        self._build_day_pills()
        if self._on_date_selected:
            self._on_date_selected(d)

    def get_selected_date(self) -> date:
        """Return selected date."""
        return self._selected
