"""
Chinese Whispers.

An implementation of the Chinese Whispers clustering algorithm.
"""

from .chinese_whispers import (
    WEIGHTING,
    aggregate_clusters,
    chinese_whispers,
    linear_weighting,
    log_weighting,
    random_argmax,
    top_weighting,
)

__version__ = "0.9.0"
__author__ = "Dmitry Ustalov"
__credits__ = ["Alexander Panchenko", "Alexander Chambers", "Frederik Wille"]
__copyright = "Copyright 2018-2024 Dmitry Ustalov"
__license__ = "MIT"

__all__ = [
    "WEIGHTING",
    "__version__",
    "aggregate_clusters",
    "chinese_whispers",
    "linear_weighting",
    "log_weighting",
    "random_argmax",
    "top_weighting",
]
