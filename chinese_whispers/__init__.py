__version__ = '0.7.2'
__author__ = 'NLPub'
__credits__ = ['Dmitry Ustalov', 'Alexander Panchenko', 'Alexander Chambers']
__license__ = 'MIT'

from .chinese_whispers import WEIGHTING, top_weighting, lin_weighting, log_weighting
from .chinese_whispers import chinese_whispers, random_argmax, aggregate_clusters
