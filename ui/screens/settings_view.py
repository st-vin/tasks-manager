"""Settings page: profile, toggles (Notifications, Student Mode, dark/light), Danger Zone."""

from typing import Callable, Optional

import customtkinter as ctk

from ui.theme import (
    BG_DARK,
    BG_CARD,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    TEXT_MUTED,
    ACCENT_MINT_LIGHT,
    ACCENT_RED,
    CORNER_RADIUS,
    FONT_HEADING,
    FONT_BODY,
    FONT_SMALL,
)


class SettingsView(ctk.CTkScrollableFrame):
    """
    Settings: header "Settings", profile (avatar, name, subtext), App Settings toggles,
    Notification Types list, Danger Zone (Delete All Data), footer version.
    """

    def __init__(
        self,
        master: ctk.CTk,
        on_back: Optional[Callable[[], None]] = None,
        on_notifications_toggle: Optional[Callable[[bool], None]] = None,
        on_student_mode_toggle: Optional[Callable[[bool], None]] = None,
        on_dark_mode_toggle: Optional[Callable[[bool], None]] = None,
        on_delete_all: Optional[Callable[[], None]] = None,
        **kwargs,
    ) -> None:
        super().__init__(master, fg_color=BG_DARK, **kwargs)
        self._on_back = on_back
        self._on_notifications = on_notifications_toggle
        self._on_student = on_student_mode_toggle
        self._on_dark = on_dark_mode_toggle
        self._on_delete_all = on_delete_all
        self._build_ui()

    def _build_ui(self) -> None:
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=16, pady=(16, 8))
        if self._on_back:
            ctk.CTkButton(
                header,
                text="←",
                width=40,
                height=40,
                fg_color="transparent",
                hover_color=BG_CARD,
                command=self._on_back,
            ).pack(side="left", padx=(0, 8))
        ctk.CTkLabel(
            header,
            text="Settings",
            font=FONT_HEADING,
            text_color=TEXT_PRIMARY,
        ).pack(side="left")

        # Profile
        profile = ctk.CTkFrame(self, fg_color="transparent")
        profile.pack(fill="x", padx=16, pady=16)
        avatar = ctk.CTkLabel(
            profile,
            text="👤",
            width=64,
            height=64,
            fg_color=ACCENT_MINT_LIGHT,
            corner_radius=32,
            font=(FONT_BODY[0], 28),
            text_color="#121D2D",
        )
        avatar.pack(side="left", padx=(0, 16))
        self._name_label = ctk.CTkLabel(
            profile,
            text="User",
            font=FONT_HEADING,
            text_color=TEXT_PRIMARY,
            anchor="w",
        )
        self._name_label.pack(anchor="w")
        self._subtext_label = ctk.CTkLabel(
            profile,
            text="Local account",
            font=FONT_SMALL,
            text_color=TEXT_MUTED,
            anchor="w",
        )
        self._subtext_label.pack(anchor="w")

        # App Settings
        app_frame = ctk.CTkFrame(self, fg_color="transparent")
        app_frame.pack(fill="x", padx=16, pady=8)
        ctk.CTkLabel(
            app_frame,
            text="App Settings",
            font=FONT_BODY,
            text_color=TEXT_SECONDARY,
        ).pack(anchor="w", pady=(0, 8))
        row1 = ctk.CTkFrame(app_frame, fg_color="transparent")
        row1.pack(fill="x", pady=4)
        ctk.CTkLabel(row1, text="Notifications", font=FONT_BODY, text_color=TEXT_PRIMARY).pack(side="left")
        self._notif_switch = ctk.CTkSwitch(
            row1,
            text="",
            onvalue=True,
            offvalue=False,
            progress_color=ACCENT_MINT_LIGHT,
            command=self._on_notif_toggle,
        )
        self._notif_switch.pack(side="right")
        self._notif_switch.select()
        row2 = ctk.CTkFrame(app_frame, fg_color="transparent")
        row2.pack(fill="x", pady=4)
        ctk.CTkLabel(row2, text="Student Mode", font=FONT_BODY, text_color=TEXT_PRIMARY).pack(side="left")
        self._student_switch = ctk.CTkSwitch(
            row2,
            text="",
            onvalue=True,
            offvalue=False,
            progress_color=ACCENT_MINT_LIGHT,
            command=self._on_student_toggle,
        )
        self._student_switch.pack(side="right")
        row3 = ctk.CTkFrame(app_frame, fg_color="transparent")
        row3.pack(fill="x", pady=4)
        ctk.CTkLabel(row3, text="Dark mode", font=FONT_BODY, text_color=TEXT_PRIMARY).pack(side="left")
        self._dark_switch = ctk.CTkSwitch(
            row3,
            text="",
            onvalue=True,
            offvalue=False,
            progress_color=ACCENT_MINT_LIGHT,
            command=self._on_dark_toggle,
        )
        self._dark_switch.pack(side="right")
        self._dark_switch.select()

        # Notification Types (sub-settings)
        notif_frame = ctk.CTkFrame(self, fg_color="transparent")
        notif_frame.pack(fill="x", padx=16, pady=16)
        ctk.CTkLabel(
            notif_frame,
            text="Notification Types",
            font=FONT_BODY,
            text_color=TEXT_SECONDARY,
        ).pack(anchor="w", pady=(0, 8))
        sub = ctk.CTkFrame(notif_frame, fg_color="transparent")
        sub.pack(fill="x", pady=4)
        ctk.CTkLabel(sub, text="🔔 In-app", font=FONT_SMALL, text_color=TEXT_PRIMARY).pack(side="left")
        ctk.CTkLabel(sub, text="Enabled", font=FONT_SMALL, text_color="#FF9F1C").pack(side="right")

        # Danger Zone
        danger = ctk.CTkFrame(self, fg_color="transparent")
        danger.pack(fill="x", padx=16, pady=16)
        ctk.CTkLabel(
            danger,
            text="Danger Zone",
            font=FONT_BODY,
            text_color=ACCENT_RED,
        ).pack(anchor="w", pady=(0, 8))
        del_row = ctk.CTkFrame(danger, fg_color="transparent")
        del_row.pack(fill="x", pady=4)
        ctk.CTkButton(
            del_row,
            text="🗑  Delete All Data",
            font=FONT_BODY,
            fg_color=ACCENT_RED,
            hover_color="#cc3d3d",
            text_color=TEXT_PRIMARY,
            corner_radius=CORNER_RADIUS,
            command=self._on_delete_all or (lambda: None),
        ).pack(side="left")

        # Footer version
        footer = ctk.CTkFrame(self, fg_color="transparent")
        footer.pack(fill="x", padx=16, pady=24)
        ctk.CTkLabel(
            footer,
            text="v1.0.0",
            font=FONT_SMALL,
            text_color=TEXT_MUTED,
        ).pack(side="right")

    def _on_notif_toggle(self) -> None:
        if self._on_notifications:
            self._on_notifications(self._notif_switch.get())

    def _on_student_toggle(self) -> None:
        if self._on_student:
            self._on_student(self._student_switch.get())

    def _on_dark_toggle(self) -> None:
        if self._on_dark:
            self._on_dark(self._dark_switch.get())

    def set_user_name(self, name: str) -> None:
        self._name_label.configure(text=name)

    def set_notifications(self, enabled: bool) -> None:
        if enabled:
            self._notif_switch.select()
        else:
            self._notif_switch.deselect()

    def set_student_mode(self, enabled: bool) -> None:
        if enabled:
            self._student_switch.select()
        else:
            self._student_switch.deselect()

    def set_dark_mode(self, enabled: bool) -> None:
        if enabled:
            self._dark_switch.select()
        else:
            self._dark_switch.deselect()
