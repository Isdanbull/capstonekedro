"""
This is a boilerplate pipeline 'preprocessing'
generated using Kedro 0.18.4
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import (
    combine_years,
    new_cols,
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
                inputs={
                    'combined_data': 'all_years_raw_data',
                    'parameters': 'params:preprocessing.new_cols.score'
                },
                outputs='preprocessed_data',
                name='new_cols_node',
            ),

        ],
        outputs='preprocessed_data'
    )
