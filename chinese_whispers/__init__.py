"""
Chinese Whispers.

An implementation of the Chinese Whispers clustering algorithm.
"""

from .chinese_whispers import (
    UnknownWeightingError,
    Weighting,
    aggregate_clusters,
    chinese_whispers,
    linear_weighting,
    log_weighting,
    random_argmax,
    top_weighting,
)

__version__ = "0.10.0.rc1"
__author__ = "Dmitry Ustalov"
__credits__ = ["Alexander Panchenko", "Alexander Chambers", "Frederik Wille"]
__copyright = "Copyright 2018-2026 Dmitry Ustalov"
__license__ = "MIT"

__all__ = [
    "UnknownWeightingError",
    "Weighting",
    "__version__",
    "aggregate_clusters",
    "chinese_whispers",
    "linear_weighting",
    "log_weighting",
    "random_argmax",
    "top_weighting",
]
