# Two player zero-sum matrix game solver

An interactive solver for two-player zero-sum matrix games. Enter an $n \times m$
payoff matrix through a GUI and get the value of the game along with the optimal
mixed strategy for both players.

## Getting started

### Prerequisites

This project needs two things that `pip` cannot install on its own:

- **tkinter**, which is part of the Python standard library rather than a PyPI
  package. It ships with the python.org and Anaconda installers.
- **GLPK**, the linear programming solver. Pyomo is only a modelling layer — it
  builds the LP and then calls out to a separate solver executable (`glpsol`).
  That executable is a compiled binary, so it has to come from conda rather
  than pip.

Because of the second point, the most reliable setup is a conda environment:

```bash
conda create -n matrixgame python=3.12
conda activate matrixgame
conda install -c conda-forge pyomo glpk numpy pandas
```

If you don't have Anaconda or Miniconda, you can get either from
[anaconda.com](https://www.anaconda.com/download).

You can edit the code in any IDE, but run it from a terminal with this
environment activated so that Pyomo can find `glpsol` on the path. In VS Code,
press <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd>, choose
**Python: Select Interpreter**, pick the `matrixgame` environment, and then open
a fresh terminal so it activates.

To confirm the solver is visible before running anything:

```bash
glpsol --version
```

### Running the application

From the project root, with the environment activated:

```bash
python main.py
```

Run it from the project root specifically — `main.py` imports from the `gui` and
`logic` packages, and the root directory is what makes those importable.

### Usage

The application provides a GUI to easily solve a matrix game.

1. Run the application as described above.
2. Enter the matrix dimensions (rows first, then columns), and specify whether
   the row player is the maximiser or the minimiser. Usually, for a two-player,
   zero-sum game, the matrix represents the payoffs for the row player — so in
   this case, the row player is the maximiser. After entering the inputs, click
   **Enter**.
3. The application will display a scrollable canvas containing entry fields for
   the payoffs. You may need to scroll horizontally and vertically to enter all
   the values.
4. If you need to change the matrix dimensions or the maximiser/minimiser
   setting, click **Go Back!**. Otherwise, once the matrix values are entered,
   press **Enter**.
5. The application will show the value of the matrix game in a boxed output
   region starting with "Output - Game Value...". The blue **Open csv file**
   link lets you view the optimal probabilities for each strategy.

The matrix does not have to be square. The row and column players may have
different numbers of strategies. Note that when they differ, the csv currently
pads the shorter player's column with `0.0` rather than leaving it blank, so a
2 x 3 game shows a "Strategy 3" row for the row player even though the row
player only has two strategies. Read those trailing zeros as "not applicable".

#### Maximiser and minimiser

The payoff matrix is always entered from the row player's perspective:
entry $(i, j)$ is what the row player receives when they play strategy $i$ and
the column player plays strategy $j$.

Choosing **max** means the row player wants that quantity to be large and the
column player wants it small; choosing **min** reverses both. The reported game
value is always stated in terms of the matrix as entered, and the two csv
columns are labelled by which player the strategy actually belongs to, not by
the orientation of the matrix that was solved internally.

## Example

Suppose we have the following matrix:

$$
\begin{pmatrix}
2 & 3 \\
4 & 3
\end{pmatrix}
$$

Assuming the row player is the maximiser, the row player will choose strategy
*2* (the second row) since $4 > 2$ and $3 \geq 3$. If the row player chooses the
second row, the column player will choose the second column, so the value of the
game is $3$. Each player chooses the second strategy with probability $1$.

Once you've run the program, you'll see this:

<p align="center">
  <img src="screenshots/input_fields_1_none.png" alt="Empty input fields" width="500">
</p>

We can enter the matrix dimensions ($2 \times 2$) and "max" in the last entry field.

<p align="center">
  <img src="screenshots/input_fields_1_filled.png" alt="Filled-in dimension fields" width="500">
</p>

Pressing "Enter" leads to:

<p align="center">
  <img src="screenshots/input_fields_2_filled.png" alt="Matrix payoff entry grid" width="500">
</p>

Now we can enter the values of the matrix and hit "Enter":

<p align="center">
  <img src="screenshots/results_panel.png" alt="Results panel showing game value" width="500">
</p>

The value of the game is $3$, as expected. Opening the csv file gives:

<p align="center">
  <img src="screenshots/csv.png" alt="csv output of optimal strategy probabilities" width="500">
</p>

## How it works

The solver formulates the matrix game as a linear program built with Pyomo and
solved using GLPK.

For a maximising row player, the LP maximises the guaranteed value $v$ subject
to the expected payoff against every column-player strategy being at least $v$,
with the strategy probabilities non-negative and summing to 1.

The column player is solved with the *same* LP applied to the **negated**
transpose. The negation is the part that matters: the column player is
minimising, and minimising $A$ is the same as maximising $-A$. Solving the plain
transpose would put the column player in the maximising seat and return a
strategy for a different game.

When the row player is the minimiser, the two solves swap over. The transposed
matrix puts the column player in the maximising seat, so that solve yields the
*column* player's strategy and the value of the game, while the negated original
matrix yields the row player's strategy.

Because the two linear programs are duals of one another, their optimal values
are equal and opposite — a useful sanity check if you ever modify the solver.

The resulting strategies and game value are displayed in the GUI and written to
**output.csv**.

## Troubleshooting

**`ApplicationError: No executable found for solver 'glpk'`**
Pyomo is installed but the solver binary isn't. Install it with
`conda install -c conda-forge glpk` and check with `glpsol --version`.

**`ModuleNotFoundError: No module named 'gui'`**
You're running `main.py` from somewhere other than the project root. `cd` to the
root and run `python main.py` from there.

**`ModuleNotFoundError: No module named 'tkinter'`**
Your Python was built without tkinter. On Debian/Ubuntu run
`sudo apt install python3-tk`; on other platforms use the python.org or Anaconda
installer.

**The window opens but nothing happens when you press Enter**
Check the terminal you launched from. tkinter swallows exceptions raised inside
button callbacks, so the traceback appears in the console rather than on screen.

## Project structure

```
main.py               Application entry point and window setup
gui/
  input_panel_1.py    Matrix dimensions and maximiser/minimiser input
  input_panel_2.py    Scrollable payoff matrix entry grid
  results_panel.py    Game value display and csv link
logic/
  solver.py           Pyomo LP formulation and GLPK solve
  create_csv.py       Runs both players' solves and writes output.csv
```
