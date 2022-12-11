"""
This module contains utility functions for the preprocessing nodes.
"""
import pandas as pd
from typing import Dict


def calculate_score(df: pd.DataFrame, params: Dict) -> pd.Series:
    """Helper function for preprocess_data. Creates an inner function using params
    which is then applied row wise to the DataFrame
    :param
        df: The DataFrame requiring a score column.
        params: Parameter dictionary
    :return
        An integer representing the fantasy score
    """
    def row_score(row) -> int:
        score = 0
        for key, value in params.items():
            score += value * row[key]

        return score

    return df.apply(lambda row: row_score(row), axis=1)
