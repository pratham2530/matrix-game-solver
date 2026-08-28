"""
This module provides functionality to export the results to CSV format. 
It handles both row and column player strategies.
"""

import os
from typing import List, Union

import pandas as pd

from logic.solver import solve_game


def write_csv(matrix: pd.DataFrame, maxormin) -> List[Union[pd.DataFrame, str, str]]:
    """
    Generates a CSV file containing game solutions for both players.

    Args:
        matrix: A pandas DataFrame representing the payoff matrix from the
               row player's perspective. Rows represent row player strategies,
               columns represent column player strategies.

    Returns:
        A list containing:
        - DataFrame with strategy probabilities for both players
        - Title string containing the game value
        - Absolute path to the generated CSV file

    Example:
        >>> payoff_matrix = pd.DataFrame([[2, -1], [-1, 1]])
        >>> result = write_csv(payoff_matrix)
        >>> print(result[1])  # Prints "Game Value: 0.25"
    """
    maxormin = maxormin.lower()
    matrix_transposed = matrix.T

    if maxormin == "max": 
        # Solve for both players
        game_value, *row_strategies = solve_game(matrix)
        _, *col_strategies = solve_game(-matrix_transposed)

    else: 
        game_value, *col_strategies = solve_game(matrix_transposed)
        _, *row_strategies = solve_game(-matrix) 
        

    # Prepare data
    rows = [
        [
            f"Strategy {i+1}",
            row_strategies[i] if i < len(row_strategies) else 0.0,
            col_strategies[i] if i < len(col_strategies) else 0.0,
        ]
        for i in range(max(len(row_strategies), len(col_strategies)))
    ]

    # Create and save DataFrame
    df = pd.DataFrame(
        rows,
        columns=["Strategy", "Row Player Probability", "Column Player Probability"],
    )
    df.to_csv("output.csv", index=False)

    return [df, f"Game Value: {game_value}", os.path.abspath("output.csv")]
