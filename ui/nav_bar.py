"""Fixed bottom navigation bar (Phase 1 spec: ~60px, #0F1724)."""

from typing import Callable, Optional

import customtkinter as ctk

from ui.theme import BG_NAV, NAV_BAR_HEIGHT, ACCENT_MINT_LIGHT, TEXT_PRIMARY, TEXT_MUTED, FONT_SMALL


class NavBar(ctk.CTkFrame):
    """
    Bottom nav: Home, Goals, Tasks, Calendar, Settings.
    Calls on_select(tab_id) when user taps a tab.
    """

    TABS = ("home", "goals", "tasks", "calendar", "settings")

    def __init__(
        self,
        master: ctk.CTk,
        on_select: Optional[Callable[[str], None]] = None,
        **kwargs,
    ) -> None:
        super().__init__(master, fg_color=BG_NAV, height=NAV_BAR_HEIGHT, **kwargs)
        self.pack_propagate(False)
        self._on_select = on_select
        self._current: str = "home"
        self._buttons: dict[str, ctk.CTkButton] = {}
        self._build()

    def _build(self) -> None:
        inner = ctk.CTkFrame(self, fg_color="transparent")
        inner.pack(fill="both", expand=True)
        labels = [
            ("Home", "home"),
            ("Goals", "goals"),
            ("Tasks", "tasks"),
            ("Calendar", "calendar"),
            ("Settings", "settings"),
        ]
        for i, (text, tab_id) in enumerate(labels):
            btn = ctk.CTkButton(
                inner,
                text=text,
                width=80,
                height=44,
                corner_radius=8,
                fg_color="transparent",
                hover_color=ACCENT_MINT_LIGHT,
                text_color=TEXT_MUTED,
                font=FONT_SMALL,
                command=lambda t=tab_id: self._select(t),
            )
            btn.grid(row=0, column=i, padx=4, pady=8, sticky="nsew")
            inner.columnconfigure(i, weight=1)
            self._buttons[tab_id] = btn
        self._update_highlight()

    def _select(self, tab_id: str) -> None:
        self._current = tab_id
        self._update_highlight()
        if self._on_select:
            self._on_select(tab_id)

    def _update_highlight(self) -> None:
        for tid, btn in self._buttons.items():
            if tid == self._current:
                btn.configure(fg_color=ACCENT_MINT_LIGHT, text_color="#121D2D")
            else:
                btn.configure(fg_color="transparent", text_color=TEXT_MUTED)

    def set_tab(self, tab_id: str) -> None:
        """Set active tab without triggering callback."""
        if tab_id in self._buttons:
            self._current = tab_id
            self._update_highlight()
