"""
Dust Persistence Study Package

A comprehensive analysis of temporal persistence of dust-induced 
cloud microphysical anomalies over the Mediterranean Basin.

Author: Horia Camarasan
Institution: UBB
Year: 2025
"""

__version__ = "1.0.0"
__author__ = "Horia Camarasan"
__email__ = "horia.camarasan@ubbcluj.ro"

# Import main modules
from .data_acquisition import DataAcquisition
from .event_detection import DustEventDetector
from .temporal_analysis import TemporalAnalyzer
from .statistical_analysis import StatisticalAnalyzer
from .visualization import Visualization

__all__ = [
    "DataAcquisition",
    "DustEventDetector", 
    "TemporalAnalyzer",
    "StatisticalAnalyzer",
    "Visualization"
]
