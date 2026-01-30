"""Main application: bottom nav + screen switching (Home, Goals, Tasks, Calendar, Settings)."""

from datetime import date, datetime
from typing import List, Optional

import customtkinter as ctk

from ui.theme import BG_DARK, FONT_BODY
from ui.nav_bar import NavBar
from ui.presenter import TaskPresenter
from ui.goal_presenter import GoalPresenter
from ui.screens import (
    HomeDashboardView,
    GoalsView,
    TasksView,
    CalendarView,
    SettingsView,
)
from ui.wizards import NewGoalWizard, NewTaskWizard
from ui.task_dialog import TaskDialog
from models import Task, Goal
from models.enums import TaskType


class MainWindow(ctk.CTk):
    """
    Main window: Deep Navy background, content area + fixed bottom nav.
    Screens: Home, Goals, Tasks, Calendar, Settings. Wired to TaskPresenter and GoalPresenter.
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.configure(fg_color=BG_DARK)
        self.title("Task Manager")
        self.geometry("900x700")
        self.minsize(600, 500)

        self._task_presenter = TaskPresenter()
        self._goal_presenter = GoalPresenter()
        self._task_presenter.set_on_error(self._show_error)
        self._goal_presenter.set_on_error(self._show_error)

        self._screens: dict = {}
        self._current_screen: Optional[str] = None
        self._build_ui()
        self._show_screen("home")

    def _build_ui(self) -> None:
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(fill="both", expand=True)
        content_frame.columnconfigure(0, weight=1)
        content_frame.rowconfigure(0, weight=1)

        # Home
        home = HomeDashboardView(
            content_frame,
            on_new_task=self._open_new_task,
            on_new_goal=self._open_new_goal,
            on_view_all_tasks=lambda: self._show_screen("tasks"),
        )
        home.grid(row=0, column=0, sticky="nsew")
        self._screens["home"] = home

        # Goals
        goals = GoalsView(
            content_frame,
            on_create_goal=self._open_new_goal,
        )
        goals.grid(row=0, column=0, sticky="nsew")
        goals.set_tab_callback(self._on_goals_tab)
        self._goal_presenter.set_refresh_view(
            lambda g: goals.show_goals(g, self._goal_presenter._show_active)
        )
        self._screens["goals"] = goals

        # Tasks
        tasks = TasksView(
            content_frame,
            on_new_task=self._open_new_task,
            on_back=lambda: self._show_screen("home"),
            get_presenter=lambda: self._task_presenter,
        )
        tasks.grid(row=0, column=0, sticky="nsew")
        self._task_presenter.set_refresh_view(tasks.show_tasks)
        tasks.show_tasks([])
        self._screens["tasks"] = tasks

        # Calendar
        def get_tasks_for_month(y: int, m: int) -> List[Task]:
            user = self._task_presenter.get_user()
            from datetime import timedelta
            import calendar as cal_module
            _, last = cal_module.monthrange(y, m)
            from_dt = datetime(y, m, 1)
            to_dt = datetime(y, m, last, 23, 59, 59)
            return self._task_presenter._task_service.get_tasks_for_user(
                user_id=user.user_id,
                from_date=from_dt,
                to_date=to_dt,
                include_completed=True,
                search_query=None,
            )
        calendar = CalendarView(
            content_frame,
            get_tasks_for_month=get_tasks_for_month,
            on_task_click=lambda t: self._edit_task_from_calendar(t),
        )
        calendar.grid(row=0, column=0, sticky="nsew")
        self._screens["calendar"] = calendar

        # Settings
        user = self._task_presenter.get_user()
        settings = SettingsView(
            content_frame,
            on_notifications_toggle=self._on_notifications_toggle,
            on_student_mode_toggle=self._on_student_mode_toggle,
            on_dark_mode_toggle=self._on_dark_mode_toggle,
            on_delete_all=self._on_delete_all_data,
        )
        settings.grid(row=0, column=0, sticky="nsew")
        settings.set_user_name(user.name)
        settings.set_notifications(user.preferences.enabled)
        settings.set_student_mode(user.is_student_mode)
        settings.set_dark_mode(True)
        self._screens["settings"] = settings

        # Nav bar
        nav = NavBar(self, on_select=self._show_screen)
        nav.pack(side="bottom", fill="x")
        self._nav = nav

    def _show_screen(self, tab_id: str) -> None:
        for sid, frame in self._screens.items():
            frame.grid_remove()
        if tab_id in self._screens:
            self._screens[tab_id].grid(row=0, column=0, sticky="nsew")
            self._current_screen = tab_id
            self._nav.set_tab(tab_id)
            if tab_id == "home":
                self._refresh_home()
            elif tab_id == "goals":
                self._refresh_goals()
            elif tab_id == "tasks":
                self._task_presenter.load_tasks(selected_date=date.today(), search_query="")
            elif tab_id == "calendar":
                today = date.today()
                self._screens["calendar"].set_month(today.year, today.month)
            elif tab_id == "settings":
                user = self._task_presenter.get_user()
                self._screens["settings"].set_user_name(user.name)
                self._screens["settings"].set_notifications(user.preferences.enabled)
                self._screens["settings"].set_student_mode(user.is_student_mode)

    def _refresh_home(self) -> None:
        home = self._screens.get("home")
        if not home:
            return
        user = self._task_presenter.get_user()
        pct = self._task_presenter.get_completion_rate_today()
        streaks = self._task_presenter.get_active_streaks()
        upcoming = self._task_presenter.get_upcoming_tasks(limit=10)
        home.refresh(user.name, pct, streaks, upcoming)

    def _refresh_goals(self) -> None:
        goals_view = self._screens.get("goals")
        if not goals_view:
            return
        user = self._goal_presenter.get_user()
        all_goals = self._goal_presenter._goal_service.get_all_for_user(user.user_id, include_archived=True)
        active_count = sum(1 for g in all_goals if not g.is_archived)
        archived_count = sum(1 for g in all_goals if g.is_archived)
        total_streaks = sum(g.current_streak for g in all_goals if not g.is_archived)
        goals_view.set_banner_counts(active_count, total_streaks)
        goals_view.set_tab_labels(active_count, archived_count)
        self._goal_presenter.load_goals(active_only=True)

    def _on_goals_tab(self, active: bool) -> None:
        self._goal_presenter.load_goals(active_only=active)
        goals_view = self._screens.get("goals")
        if goals_view:
            user = self._goal_presenter.get_user()
            all_goals = self._goal_presenter._goal_service.get_all_for_user(user.user_id, include_archived=True)
            active_count = sum(1 for g in all_goals if not g.is_archived)
            archived_count = sum(1 for g in all_goals if g.is_archived)
            goals_view.set_tab_labels(active_count, archived_count)

    def _open_new_goal(self) -> None:
        def save(title: str, description: str, color_hex: str) -> None:
            self._goal_presenter.create_goal(title=title, description=description, color_hex=color_hex)
            self._refresh_goals()
            self._refresh_home()

        w = NewGoalWizard(self, on_save=save, on_back=lambda: None)
        self.after(50, w.lift)
        self.after(50, w.focus_force)

    def _open_new_task(self) -> None:
        def on_type_selected(task_type: TaskType) -> None:
            def save_new(**kwargs) -> None:
                self._task_presenter.create_task(
                    title=kwargs.get("title", ""),
                    description=kwargs.get("description", ""),
                    due_date=kwargs.get("due_date"),
                    duration_minutes=kwargs.get("duration_minutes", 0),
                    priority=kwargs.get("priority"),
                    task_type=task_type,
                )
                self._refresh_home()
                if self._current_screen == "tasks":
                    self._task_presenter.load_tasks()
                if self._current_screen == "calendar":
                    self._screens["calendar"].refresh_events()

            dlg = TaskDialog(self, dialog_title="New Task", on_save=save_new)
            self.after(50, dlg.focus_force)

        w = NewTaskWizard(self, on_select_type=on_type_selected, on_back=lambda: None)
        self.after(50, w.lift)
        self.after(50, w.focus_force)

    def _edit_task_from_calendar(self, task: Task) -> None:
        def save_edit(**kwargs) -> None:
            self._task_presenter.update_task(
                kwargs["task_id"],
                title=kwargs.get("title"),
                description=kwargs.get("description"),
                due_date=kwargs.get("due_date"),
                duration_minutes=kwargs.get("duration_minutes"),
                priority=kwargs.get("priority"),
            )
            self._screens["calendar"].refresh_events()

        dlg = TaskDialog(self, dialog_title="Edit Task", on_save=save_edit)
        dlg.set_task(task)

    def _on_notifications_toggle(self, enabled: bool) -> None:
        user = self._task_presenter.get_user()
        user.update_preferences(enabled=enabled)
        self._task_presenter._user_service._repo.save(user)

    def _on_student_mode_toggle(self, enabled: bool) -> None:
        user = self._task_presenter.get_user()
        user.is_student_mode = enabled
        self._task_presenter._user_service._repo.save(user)

    def _on_dark_mode_toggle(self, enabled: bool) -> None:
        ctk.set_appearance_mode("dark" if enabled else "light")

    def _on_delete_all_data(self) -> None:
        # Confirm then delete all tasks and goals for user
        result = self._ask_confirm("Type 'DELETE' to confirm:")
        if result and result.strip().upper() == "DELETE":
            user = self._task_presenter.get_user()
            for task in self._task_presenter._task_service.get_tasks_for_user(user_id=user.user_id, include_completed=True):
                self._task_presenter._task_service.delete_task(task.task_id)
            for goal in self._goal_presenter._goal_service.get_all_for_user(user.user_id, include_archived=True):
                self._goal_presenter._goal_service.delete_goal(goal.goal_id)
            self._refresh_home()
            self._refresh_goals()
            if self._current_screen == "tasks":
                self._task_presenter.load_tasks()
            if self._current_screen == "calendar":
                self._screens["calendar"].refresh_events()
            self._show_error("All data deleted.")
        elif result is not None:
            self._show_error("Cancelled. Type DELETE to confirm.")

    def _ask_confirm(self, prompt: str) -> Optional[str]:
        """Simple dialog: entry + OK/Cancel. Returns entry value or None."""
        d = ctk.CTkToplevel(self)
        d.title("Confirm")
        d.geometry("360x120")
        d.configure(fg_color=BG_DARK)
        d.transient(self)
        ctk.CTkLabel(d, text=prompt, font=FONT_BODY, text_color="white").pack(padx=20, pady=(20, 8))
        entry = ctk.CTkEntry(d, width=320, height=36)
        entry.pack(padx=20, pady=8)
        result: List[Optional[str]] = [None]

        def ok() -> None:
            result[0] = entry.get()
            d.destroy()

        def cancel() -> None:
            result[0] = ""
            d.destroy()

        btn_row = ctk.CTkFrame(d, fg_color="transparent")
        btn_row.pack(pady=(0, 16))
        ctk.CTkButton(btn_row, text="Cancel", command=cancel).pack(side="left", padx=8)
        ctk.CTkButton(btn_row, text="OK", command=ok).pack(side="left", padx=8)
        entry.bind("<Return>", lambda e: ok())
        d.transient(self)
        d.grab_set()
        self.wait_window(d)
        return result[0]

    def _show_error(self, message: str) -> None:
        err = ctk.CTkToplevel(self)
        err.title("Error")
        err.geometry("400x120")
        err.configure(fg_color=BG_DARK)
        err.transient(self)
        ctk.CTkLabel(err, text=message, font=FONT_BODY, text_color="white", wraplength=360).pack(padx=20, pady=20)
        ctk.CTkButton(err, text="OK", command=err.destroy).pack(pady=(0, 16))
