"""Search/Filter bar for tasks (title/description filter)."""

from typing import Callable, Optional

import customtkinter as ctk

from ui.theme import BG_INPUT, TEXT_PRIMARY, TEXT_SECONDARY, CORNER_RADIUS, FONT_BODY


class SearchBar(ctk.CTkFrame):
    """
    Search and filter bar: entry + optional placeholder.

    Calls on_search when text changes (debounced or on return).
    """

    def __init__(
        self,
        master: ctk.CTk,
        placeholder: str = "Search tasks...",
        on_search: Optional[Callable[[str], None]] = None,
        **kwargs,
    ) -> None:
        super().__init__(master, fg_color="transparent", **kwargs)
        self._on_search = on_search
        self._entry = ctk.CTkEntry(
            self,
            placeholder_text=placeholder,
            height=40,
            corner_radius=CORNER_RADIUS,
            fg_color=BG_INPUT,
            text_color=TEXT_PRIMARY,
            placeholder_text_color=TEXT_SECONDARY,
            font=FONT_BODY,
            border_width=0,
        )
        self._entry.pack(fill="x", padx=0, pady=0)
        self._entry.bind("<Return>", self._do_search)
        self._entry.bind("<KeyRelease>", self._on_key)

    def _do_search(self, event=None) -> None:
        if self._on_search:
            self._on_search(self._entry.get().strip())

    def _on_key(self, event=None) -> None:
        # Optional: debounce or trigger on Return only. We trigger on Return.
        pass

    def get_query(self) -> str:
        """Return current search text."""
        return self._entry.get().strip()

    def set_query(self, text: str) -> None:
        """Set search text."""
        self._entry.delete(0, "end")
        self._entry.insert(0, text)
