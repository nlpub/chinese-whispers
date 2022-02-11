__version__ = '0.7.6'
__author__ = 'Dmitry Ustalov'
__credits__ = ['Alexander Panchenko', 'Alexander Chambers', 'Frederik Wille']
__license__ = 'MIT'

from .chinese_whispers import (
    WEIGHTING,
    top_weighting,
    lin_weighting,
    log_weighting,
    chinese_whispers,
    random_argmax,
    aggregate_clusters
)

__all__ = [
    'WEIGHTING',
    'top_weighting',
    'lin_weighting',
    'log_weighting',
    'chinese_whispers',
    'random_argmax',
    'aggregate_clusters'
]
