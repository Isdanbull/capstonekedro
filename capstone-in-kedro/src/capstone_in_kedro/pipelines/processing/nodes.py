"""
This is a boilerplate pipeline 'processing'
generated using Kedro 0.18.4
"""
import pandas as pd

from typing import Dict


def filtered_data(all_data: pd.DataFrame, parameters: Dict[str:str]) -> pd.DataFrame:
    """Filters rows to select required games.
    :param
        all_data: combined years data with new columns
        parameters: Parameters defined in parameters/processing.yml
    :return:
        Preprocessed data with only player data from major regions included and games
        with unknown players excluded.
    """
    # filter the dataset to exclude team stats and minor region games
    major_players = all_data[(all_data.league.isin(parameters['leagues'])) & (all_data.position != 'team')]

    # identify games including unknown players
    game_ids_with_missing_players = major_players[major_players.playerid.isna()].gameid.unique()

    return major_players[~major_players.gameid.isin(game_ids_with_missing_players)]


def sum_stats_by_day(all_data: pd.DataFrame, params: Dict[str:Dict]) -> pd.DataFrame:
    """Creates dataframe with the sum of stats by player per day.
    :param:
        all_data: compined years data with new columns
        params: Parameters defined in parameters/processing.yml
    :return
        DataFrame grouped by playerid and date with columns summed
    """
    group_by_cols = params['group_by_cols']
    agg_cols = params['agg_cols']

    return all_data.groupby(group_by_cols)[agg_cols].sum()


def count_games_per_day(all_data: pd.DataFrame, params: Dict[str:Dict]) -> pd.DataFrame:
    """Creates dataframe with count of number of games each player played each day.
    :param:
        all_data: combined years data with new columns
        params: Parameters defined in parameters/processing.yml
    :return:
        DataFrame grouped by playerid and date with playerid's counted.
    """
    group_by_cols = params['group_by_cols']
    agg_cols = params['agg_cols']

    return all_data.groupby(group_by_cols)[agg_cols].count()


