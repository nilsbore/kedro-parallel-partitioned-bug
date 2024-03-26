"""Project pipelines."""
from __future__ import annotations
from typing import Dict, Any, Callable

from kedro.pipeline import Pipeline, node


def create_dict() -> Dict[str, Any]:
    return {"test": "test"}


def create_partitioned() -> Dict[str, Callable[[], Dict[str, Any]]]:
    return {f"file_{i}": create_dict for i in range(0, 5)}


def consume_both(a, b):
    return a


def create_pipeline() -> Pipeline:
    return Pipeline(
        [
            node(func=create_partitioned, inputs=[], outputs="a", name="create_a_node"),
            node(func=create_partitioned, inputs=[], outputs="b", name="create_b_node"),
            node(
                func=consume_both,
                inputs=["a", "b"],
                outputs="c",
                name="consume_both_node",
            ),
        ]
    )


def register_pipelines() -> dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from pipeline names to ``Pipeline`` objects.
    """
    pipelines = {"__default__": create_pipeline()}
    return pipelines
