"""
Data export system with multiple format support.
"""

import json
import csv
from pathlib import Path
from typing import Dict, List, Optional, Any
from ..core.base_component import BaseComponent


class DataExporter(BaseComponent):
    """
    Multi-format data exporter.
    """
    
    def __init__(self, config: Dict = None):
        """Initialize the data exporter."""
        super().__init__("data_exporter", config)
        
    def initialize(self) -> bool:
        """Initialize the data exporter."""
        self.is_initialized = True
        return True
    
    def cleanup(self) -> bool:
        """Clean up data exporter."""
        return True
    
    def export_data(self, data: List[Dict], filename: str, format: str = "csv") -> bool:
        """Export data to specified format."""
        try:
            output_dir = Path("output")
            output_dir.mkdir(exist_ok=True)
            
            filepath = output_dir / filename
            
            if format.lower() == "csv":
                return self._export_csv(data, filepath)
            elif format.lower() == "json":
                return self._export_json(data, filepath)
            else:
                self.logger.error(f"Unsupported format: {format}")
                return False
                
        except Exception as e:
            self.logger.error(f"Export failed: {e}")
            return False
    
    def _export_csv(self, data: List[Dict], filepath: Path) -> bool:
        """Export data to CSV format."""
        try:
            if not data:
                return False
            
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = data[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            
            self.logger.info(f"Data exported to CSV: {filepath}")
            return True
            
        except Exception as e:
            self.logger.error(f"CSV export failed: {e}")
            return False
    
    def _export_json(self, data: List[Dict], filepath: Path) -> bool:
        """Export data to JSON format."""
        try:
            with open(filepath, 'w', encoding='utf-8') as jsonfile:
                json.dump(data, jsonfile, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Data exported to JSON: {filepath}")
            return True
            
        except Exception as e:
            self.logger.error(f"JSON export failed: {e}")
            return False
