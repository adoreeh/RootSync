"""
RootSync - Newton-Raphson Visual Root Finder
=============================================
A modern engineering dashboard for root finding using the Newton-Raphson method.

Run with: python main.py

Structure:
- main.py   : Entry point
- solver.py : Newton-Raphson computation logic
- ui.py     : Modern UI/UX layer
- styles.py : Theme configuration
"""

import tkinter as tk
from ui import RootSyncApp


def main():
    """Main entry point for RootSync application"""
    root = tk.Tk()
    app = RootSyncApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()