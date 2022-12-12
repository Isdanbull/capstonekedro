"""
This is a boilerplate pipeline 'preprocessing'
generated using Kedro 0.18.4
"""
import pandas as pd
from typing import Dict

from .utils import calculate_score


def combine_years(*args) -> pd.DataFrame:
    """Unions all year's data into a single dataset
    :param
        args: Several dataframes
    :return:
        A single pandas DatFrame
    """
    return pd.concat(list(args), axis=0, join='outer', ignore_index=True)


def new_cols(combined_data: pd.DataFrame, parameters: Dict[str:float]) -> pd.DataFrame:
    """Creates derived columns needed for model. 'side_pos' which combines players position
    with which side they are on (Blue or Red)
    :param
        combined_data: combined yearly data.
        parameters: Parameters defined in parameters/preprocessing.yml
    :return
        Dataframe with new columns created
    """
    combined_data['side_pos'] = combined_data.side + combined_data.position
    combined_data['score'] = calculate_score(combined_data, parameters['score'])

    return combined_data






