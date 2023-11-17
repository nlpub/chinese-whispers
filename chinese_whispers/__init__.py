"""
Chinese Whispers

An implementation of the Chinese Whispers clustering algorithm.
"""

from .chinese_whispers import (
    WEIGHTING,
    top_weighting,
    linear_weighting,
    log_weighting,
    chinese_whispers,
    random_argmax,
    aggregate_clusters
)

__version__ = '0.8.2.post2'
__author__ = 'Dmitry Ustalov'
__credits__ = ['Alexander Panchenko', 'Alexander Chambers', 'Frederik Wille']
__copyright = 'Copyright 2018-2023 Dmitry Ustalov'
__license__ = 'MIT'

__all__ = [
    '__version__',
    'WEIGHTING',
    'top_weighting',
    'linear_weighting',
    'log_weighting',
    'chinese_whispers',
    'random_argmax',
    'aggregate_clusters'
]
