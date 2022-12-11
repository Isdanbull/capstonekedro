"""
This is a boilerplate pipeline 'preprocessing'
generated using Kedro 0.18.4
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import (
    combine_years,
    new_cols,
    filtered_data
)


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=combine_years,
                inputs=["2014_raw_data", "2015_raw_data", "2016_raw_data", "2017_raw_data", "2018_raw_data",
                        "2019_raw_data", "2020_raw_data", "2021_raw_data", "2022_raw_data"],
                outputs='all_years_raw_data',
                name='combine_years_node',
            ),
            node(
                func=new_cols,
                inputs=['all_years_raw_data', 'parameters'],
                outputs='data_with_extra_cols',
                name='new_cols_node',
            ),
            node(
                func=filtered_data,
                inputs=['data_with_extra_cols', 'parameters'],
                outputs='preprocessed_data',
                name='filtering_node',
            ),
        ],
        outputs='preprocessed_data'
    )
