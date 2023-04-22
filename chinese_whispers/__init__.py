__version__ = '0.8.2.pre1'
__author__ = 'Dmitry Ustalov'
__credits__ = ['Alexander Panchenko', 'Alexander Chambers', 'Frederik Wille']
__license__ = 'MIT'

from .chinese_whispers import (
    WEIGHTING,
    top_weighting,
    linear_weighting,
    log_weighting,
    chinese_whispers,
    random_argmax,
    aggregate_clusters
)

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
