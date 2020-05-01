"""
This module contains various statistical helper functions
"""

from .stats import gauss_sigma_to_prob, get_poisson_confidence_interval
from .hist  import get_histogram_statistics

__all__ = [
    'gauss_sigma_to_prob', 'get_poisson_confidence_interval',
    'get_histogram_statistics'
]

