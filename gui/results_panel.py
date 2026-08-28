"""
This module contains the Results Panel frame class. 
It displays the game value and csv output containing the mixed strategies for each player. 
"""

from tkinter import Frame, Label, Button, messagebox
from typing import Dict, Any, TypedDict, List

import os
import subprocess
import sys
import numpy as np

from logic.create_csv import write_csv


class WidgetGroups(TypedDict):
    """
    Type-hinted container for organized GUI widgets.

    Groups widgets by type for structured access:
    - labels: Text display widgets (Dict[str, Label])
    - buttons: Interactive buttons (Dict[str, Button])
    - frames: Container frames (Dict[str, Frame])
    """

    labels: Dict[str, Label]
    buttons: Dict[str, Button]
    frames: Dict[str, Frame]


class Results_Panel(Frame):
    """
    The third frame of the application, responsible for displaying game solutions.
    It shows the calculated strategies and provides options to view CSV results.

    Attributes:
        app: Reference to parent application
        rows: Number of rows in the matrix
        cols: Number of columns in the matrix
        maxormin: Player role ('max' or 'min')
        matrix: The game matrix data
        csv_path: Path to the generated CSV file
        widgets: Dictionary organizing all UI components
    """

    def __init__(self, parent: Any) -> None:
        """
        Initialize the solution display frame and setup UI components.

        Args:
            parent: The parent container (typically the root Tk window)
        """
        super().__init__(parent)
        self.app = parent

        # Game parameters
        self.rows = 0
        self.cols = 0
        self.maxormin = ""
        self.matrix: np.ndarray = np.array([])
        self.csv_path = ""

        # Widget containers
        self.widgets: WidgetGroups = {"labels": {}, "buttons": {}, "frames": {}}

        self._setup_ui()

    def _setup_ui(self) -> None:
        """
        Initialize all UI components and layout.
        """
        # Create frames
        self._create_frames()

        # Create widgets
        self._create_labels()
        self._create_buttons()

        # Setup layout
        self._setup_layout()

    def _create_frames(self) -> None:
        """
        Create frame widgets.
        """
        self.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.widgets["frames"]["input"] = Frame(
            self,
            borderwidth=1,
            padx=15,
            pady=70,
            highlightbackground="black",
            highlightthickness=1,
        )
        self.widgets["frames"]["output"] = Frame(
            self.widgets["frames"]["input"],
            borderwidth=1,
            padx=10,
            pady=10,
            highlightbackground="black",
            highlightthickness=1,
        )

    def _create_labels(self) -> None:
        """
        Create label widgets.
        """
        self.widgets["labels"] = {
            "title": Label(self.widgets["frames"]["input"], text="Solution:"),
            "inputs": Label(self.widgets["frames"]["input"], text=""),
            "output": Label(self.widgets["frames"]["output"], text=""),
            "instructions": Label(
                self.widgets["frames"]["output"],
                text="Click the link below to view the mixed strategies for both players.",
            ),
            "csv_link": Label(
                self.widgets["frames"]["output"],
                text="Open csv file",
                fg="blue",
                cursor="hand2",
            ),
        }
        self.widgets["labels"]["csv_link"].bind("<Button-1>", lambda e: self.open_csv())
        self.widgets["labels"]["csv_link"].grid_remove()

    def _create_buttons(self) -> None:
        """
        Create button widgets.
        """
        self.widgets["buttons"] = {
            "restart": Button(
                self.widgets["frames"]["input"], text="Restart", command=self.restart
            )
        }

    def _setup_layout(self) -> None:
        """
        Arrange widgets in grid layout.
        """
        # Frames
        self.widgets["frames"]["input"].grid(
            row=0, column=0, sticky="nsew", padx=5, pady=5
        )
        self.widgets["frames"]["output"].grid(
            row=2, column=0, sticky="nsew", padx=10, pady=10
        )

        # Labels
        self.widgets["labels"]["title"].grid(row=0, column=0)
        self.widgets["labels"]["inputs"].grid(row=1, column=0)
        self.widgets["labels"]["output"].grid(row=2, column=0)
        self.widgets["labels"]["instructions"].grid(row=3, column=0)
        self.widgets["labels"]["csv_link"].grid(row=4, column=0, pady=5)

        # Buttons
        self.widgets["buttons"]["restart"].grid(row=5, column=0)

    def update_inputs(
        self, rows: int, cols: int, maxormin: str, matrix: List[List[float]]
    ) -> None:
        """
        Update the display with new game parameters and matrix.

        Args:
            rows: Number of rows in the matrix
            cols: Number of columns in the matrix
            maxormin: Player type ("max" or "min")
            matrix: The game matrix data
        """
        self.rows = rows
        self.cols = cols
        self.maxormin = maxormin
        self.matrix = np.array(matrix)

        self.widgets["labels"]["inputs"].config(
            text=f"Inputs - Rows: {self.rows}, Columns: {self.cols}, "
            f"Row player: {self.maxormin}imiser"
        )

        self.run_solver(self.matrix)

    def run_solver(self, matrix: np.ndarray) -> None:
        """
        Run the game solver and update the output display.

        Args:
            matrix: The game matrix to solve
        """
        out = write_csv(matrix, self.maxormin)
        self.widgets["labels"]["output"].config(text=f"Output - {out[1]}")
        self.csv_path = out[2]
        self.widgets["labels"]["csv_link"].grid()

    def open_csv(self) -> None:
        """
        Open the generated CSV file with the default application.
        Shows error message if file cannot be opened.
        """
        try:
            if os.name == "nt":
                os.startfile(self.csv_path)
            elif sys.platform == "darwin":
                subprocess.run(["open", self.csv_path], check=True)
            else:
                subprocess.run(["xdg-open", self.csv_path], check=True)
        except (OSError, subprocess.SubprocessError) as e:
            messagebox.showerror("Error", f"Could not open csv file: {e}")

    def restart(self) -> None:
        """
        Reset the application and return to the Input Panel 1 window.
        """
        self.app.first.clear_entries()
        self.app.first.tkraise()


