"""
This module contains the main application class.
It initializes the main window, sets up the user interface, and handles
window positioning.
"""

from tkinter import Tk

from gui.input_panel_1 import Input_Panel_1
from gui.input_panel_2 import Input_Panel_2
from gui.results_panel import Results_Panel


class App(Tk):
    """
    The main application class.

    This class inherits from tkinter.Tk and is responsible for creating
    the root window, setting up its properties, and initializing the
    main user interface.
    """

    def __init__(self):
        """
        Initializes the application window.
        """
        super().__init__()

        self.title("Matrix Game Solver")
        self.resizable(False, False)

        # Fonts for consistent styling
        self.font = ("Segoe UI", 9, "normal")
        self.error_font = ("Segoe UI", 8, "normal")

        # Create and initialize all GUI windows
        self.first = Input_Panel_1(self)
        self.second = Input_Panel_2(self)
        self.third = Results_Panel(self)

        # Place the main frame on top
        self.first.tkraise()
        self.center_window()
        self.mainloop()

    def center_window(self):
        """
        Centers the application window on the screen.

        This method calculates the necessary x and y coordinates to
        position the window in the middle of the user's screen.
        """
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_coord = (screen_width // 2) - (width // 2)
        y_coord = (screen_height // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x_coord}+{y_coord}")


if __name__ == "__main__":
    App()


