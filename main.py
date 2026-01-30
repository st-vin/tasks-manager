"""Entry point for the Task Management application."""

import sys
from pathlib import Path

# Ensure project root is on path (for running as script or PyInstaller bundle)
_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))


def main() -> None:
    """Launch the CustomTkinter main window."""
    from ui.main_window import MainWindow

    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
