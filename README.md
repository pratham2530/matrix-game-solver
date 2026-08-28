# Two-player zero-sum matrix game solver

An interactive solver for two-player zero-sum matrix games. Enter an $n \times m$
payoff matrix through a GUI and obtain the value of the game with the optimal
mixed strategies for both players.

## Getting started

### Prerequisites

`pip` can't install these: 

- **tkinter** (part of the Python standard library). 
- **GLPK** (the linear programming solver). Pyomo builds the LP and
  then calls out to a separate solver executable (`glpsol`).

Hence the recommended setup is a conda environment:

```bash
conda create -n matrixgame python=3.12
conda activate matrixgame
conda install -c conda-forge pyomo glpk numpy pandas
```

If you don't have Anaconda or Miniconda, you can get either from
[anaconda.com](https://www.anaconda.com/download).

### Running the application

Run from the project root specifically since `main.py` imports from the `gui` and
`logic` packages: 

```bash
conda activate matrixgame
python main.py
```

### Usage

1. Run the application as described above.
2. Enter the matrix dimensions (rows first, then columns), and specify whether
   the row player is the maximiser or the minimiser. Usually, for a two-player
   zero-sum game the matrix represents the payoffs for the row player (in this
   case, the row player would be the "maximiser").
    After entering the inputs, click **Enter**.
3. The application will display a scrollable canvas containing entry fields for
   the payoffs. You may need to scroll horizontally and vertically to enter all
   the values.
4. If you need to change the matrix dimensions or the maximiser/minimiser
   setting, click **Go Back!**. Once the matrix values are entered
   press **Enter**.
5. The application will show the value of the matrix game in a boxed output
   region starting with "Output - Game Value...". The blue **Open csv file**
   link lets you view the optimal probabilities for each strategy.

The matrix does not have to be square. The row and column players may have
different numbers of strategies. Note that when they differ, the csv currently
pads the shorter player's column with `0.0` rather than leaving it blank, so a
2 x 3 game shows a "Strategy 3" row for the row player even though the row
player only has two strategies. 

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

Then, the column player is solved with the *same* LP applied to the **negated**
transpose. The negation is needed since the column player is now the minimising player. 

For a minimising column player, the reverse of the above occurs. 

## Troubleshooting

**`ApplicationError: No executable found for solver 'glpk'`**
Pyomo is installed but the solver binary isn't. Install it with
`conda install -c conda-forge glpk` and check with `glpsol --version`.

## Project structure

```
main.py               Application set up
gui/
  input_panel_1.py    Matrix dimensions and maximiser/minimiser input
  input_panel_2.py    Scrollable payoff matrix entry grid
  results_panel.py    Game value display and csv link
logic/
  solver.py           Pyomo LP formulation and GLPK solver
  create_csv.py       Runs both players' solves and writes output.csv
```
