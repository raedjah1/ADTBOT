"""
Data handling module for SmartWebBot

Contains data extraction, processing, and export functionality.
"""

from .extractor import DataExtractor
from .exporter import DataExporter
from .processor import DataProcessor

__all__ = ["DataExtractor", "DataExporter", "DataProcessor"]
