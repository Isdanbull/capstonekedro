"""
This is a boilerplate pipeline 'processing'
generated using Kedro 0.18.4
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import (
    filtered_data
)


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=filtered_data,
            inputs={
                'all_data': 'data_with_extra_cols',
                'parameters': 'params:filtered_data'},
            outputs='filtered_data',
            name='filtering_node',
        ),
        node(
            name='aggregation'
        ),
        node(
            name=''
        )
    ])
