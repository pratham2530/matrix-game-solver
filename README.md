# Two player zero-sum matrix game solver

## Getting started

### Prerequisites

Ensure you have Python 3.x installed. The dependencies are listed in `requirements.txt`. You can install them using pip:

```bash
pip install -r requirements.txt
```

Note: requirements.txt covers the Python packages, but the GLPK solver itself is a separate system-level dependency which can be installed via conda. =

This project relies on the Pyomo optimization package and the GLPK solver. While you can edit the code in any IDE, Pyomo needs to be able to find the GLPK solver executable on your system path. The most reliable way to get both installed correctly is via conda:

```bash
conda install -c conda-forge pyomo glpk
```

If you don't have Anaconda installed, you can get it from anaconda.com. Once Pyomo and GLPK are installed in your conda environment, activate that environment and run the program from its terminal.

### Running the application

In Anaconda Navigator, check whether the **Pyomo** package is installed. In the "Environments" section, search for the **Pyomo** package and install it if needed. Then launch a Python IDE and run:

```bash
python main.py
```

### Usage

The application provides a GUI to easily solve a matrix game.

1. Run the application as described above.
2. Enter the matrix dimensions (rows first, then columns), and specify whether the row player is the maximiser or the minimiser. Usually, for a two-player, zero-sum game, the matrix represents the payoffs for the row player — so in this case, the row player is the maximiser. After entering the inputs, click **Enter**.
3. The application will display a scrollable canvas containing entry fields for the payoffs. You may need to scroll horizontally and vertically to enter all the values.
4. If you need to change the matrix dimensions or the maximiser/minimiser setting, click **Go Back!**. Otherwise, once the matrix values are entered, press **Enter**.
5. The application will show the value of the matrix game in a boxed output region starting with "Output - Game Value...". The blue **Open csv file** link lets you view the optimal probabilities for each strategy.

The application will then display the full solution, including the optimal strategies for both players and the value of the game.

## Example

Suppose we have the following matrix:

$$
\begin{pmatrix}
2 & 3 \\
4 & 3
\end{pmatrix}
$$

Assuming the row player is the maximiser, the row player will choose strategy *2* (the second row) since $4 > 2$ and $3 \geq 3$. If the row player chooses the second row, the column player will choose the second column, so the value of the game is $3$. Each player chooses the second strategy with probability $1$.

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
The solver formulates the matrix game as a linear program (LP) built with Pyomo and solved using GLPK. For the row player, it maximizes the guaranteed game value $v$ subject to the constraint that the expected payoff against every column-player strategy is at least $v$, and that the row player's strategy probabilities are non-negative and sum to 1. The column player's optimal strategy is found by solving the same LP on the transposed payoff matrix. The resulting strategies and game value are displayed in the GUI and written to **output.csv**.
