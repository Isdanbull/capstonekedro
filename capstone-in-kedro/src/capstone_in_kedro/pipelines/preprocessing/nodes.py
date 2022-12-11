"""
This is a boilerplate pipeline 'preprocessing'
generated using Kedro 0.18.4
"""
import pandas as pd
from typing import Dict, List

from .utils import calculate_score


def combine_years(a, b, c, d, e, f, g, h, i) -> pd.DataFrame:
    """Unions all year's data into a single dataset
    :param
        parameters: Parameters defined in parameters/preprocessing.yml
    :return:
        A single pandas DatFrame
    """
    raw_data = [a,b,c,d,e,f,g,h,i]
    return pd.concat(raw_data, axis=0, join='outer', ignore_index=True)


def new_cols(combined_data: pd.DataFrame, parameters: Dict) -> pd.DataFrame:
    """Creates derived columns needed for model. 'side_pos' which combines players position
    with which side they are on (Blue or Red)
    :param
        combined_data: combined yearly data.
        parameters: Parameters defined in parameters/preprocessing.yml
    :return
        Dataframe with new columns created
    """
    combined_data['side_pos'] = combined_data.side + combined_data.position
    combined_data['score'] = calculate_score(combined_data, parameters['preprocessing']['new_cols']['score'])

    return combined_data


def filtered_data(all_data: pd.DataFrame, parameters: Dict) -> pd.DataFrame:
    """Filters rows to select required games.
    :param
        all_data: combined years data with new columns
        parameters: Parameters defined in parameters/preprocessing.yml
    :return:
        Preprocessed data with only player data from major regions included and games
        with unknown players excluded.
    """
    # filter the dataset to exclude team stats and minor region games
    major_players = all_data[(all_data.league.isin(parameters['preprocessing']['preprocess_data']['leagues'])) & (all_data.position != 'team')]

    # identify games including unknown players
    game_ids_with_missing_players = major_players[major_players.playerid.isna()].gameid.unique()

    return major_players[~major_players.gameid.isin(game_ids_with_missing_players)]



