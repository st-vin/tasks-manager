"""Theme and styling: Deep Navy design system (Phase 1 spec)."""

from typing import Tuple

# Primary background
BG_DARK = "#121D2D"           # Deep Navy (primary background)
BG_CARD = "#1A2639"           # Lighter Navy (secondary/card)
BG_NAV = "#0F1724"            # Darker (fixed bottom nav)
BG_INPUT = "#1A2639"          # Entry/card
BG_SIDEBAR = "#152030"        # Calendar event sidebar

# Accents
ACCENT_MINT_LIGHT = "#B7E4C7"   # Mint Green (primary action, selected)
ACCENT_MINT = "#52B788"         # Vibrant mint
ACCENT_ORANGE = "#FF9F1C"       # Streaks
ACCENT_ORANGE_DARK = "#FF4D00"
ACCENT_PURPLE = "#8A2BE2"       # Goals header
ACCENT_PURPLE_CAL = "#7B68EE"   # Calendar pills
ACCENT_RED = "#FF4D4D"          # Danger/warnings
ACCENT_TEAL = "#00CED1"         # Calendar/event
ACCENT_BLUE = "#4169E1"
ACCENT_PINK = "#FF6B6B"
ACCENT_TASK_CARD = "#D0F0C0"    # Light green task card

# Text
TEXT_PRIMARY = "#ffffff"
TEXT_SECONDARY = "#a0aec0"
TEXT_MUTED = "#718096"
TEXT_GREY = "#A0A0A0"

# Legacy status colors (aligned with spec)
STATUS_COMPLETED = ACCENT_MINT_LIGHT
STATUS_REJECTED = "#5b9bd5"
STATUS_RUNNING = "#b8a9c9"
STATUS_UPCOMING = ACCENT_MINT_LIGHT
STATUS_OVERDUE = "#e07c7c"

# UI
CORNER_RADIUS = 12
CARD_CORNER_RADIUS = 16
BUTTON_RADIUS = 8
INPUT_HEIGHT = 40
HEADER_HEIGHT = 56
NAV_BAR_HEIGHT = 60

# Fonts (Inter, Roboto, or Segoe UI)
FONT_FAMILY = "Segoe UI"
FONT_TITLE = (FONT_FAMILY, 18, "bold")
FONT_HEADING = (FONT_FAMILY, 16, "bold")
FONT_HEADING_LARGE = (FONT_FAMILY, 24, "bold")
FONT_BODY = (FONT_FAMILY, 13)
FONT_SMALL = (FONT_FAMILY, 11)
FONT_CAPTION = (FONT_FAMILY, 10)

# Timeline
TIMELINE_LABEL_WIDTH = 60
TIME_MARKER_COLOR = TEXT_MUTED


def status_to_color(status: str) -> str:
    """Map task status to card background color."""
    s = status.lower() if status else ""
    if "completed" in s:
        return ACCENT_TASK_CARD  # Light green per spec
    if "rejected" in s or "cancelled" in s:
        return STATUS_REJECTED
    if "in_progress" in s or "running" in s:
        return STATUS_RUNNING
    if "upcoming" in s or "today" in s or "pending" in s or "scheduled" in s:
        return ACCENT_TASK_CARD
    if "overdue" in s:
        return STATUS_OVERDUE
    return ACCENT_TASK_CARD
