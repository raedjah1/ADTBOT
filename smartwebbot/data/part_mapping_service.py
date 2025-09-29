"""
Part Number Mapping Service

Manages part number mappings for the Unit Receiving ADT system.
Provides search, add, and management functionality for part conversions.
"""

import json
import os
from typing import List, Dict, Any, Optional
from datetime import datetime
from ..utils.logger import get_logger


class PartMappingService:
    """Service for managing part number mappings."""
    
    def __init__(self, data_file: Optional[str] = None):
        """Initialize the service."""
        self.logger = get_logger(__name__)
        
        # Default data file location
        self.data_file = data_file or os.path.join(
            os.path.dirname(__file__), '..', '..', 'data', 'part_mappings.json'
        )
        
        # Ensure data directory exists
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        
        # Initialize with default mappings if file doesn't exist
        self._initialize_default_mappings()
    
    def _initialize_default_mappings(self):
        """Initialize with default part mappings if no data file exists."""
        if not os.path.exists(self.data_file):
            self.logger.info("Initializing default part mappings")
            
            default_mappings = [
                # Basic conversions (remove prefixes, etc.)
                {"original": "SA5816", "processAs": "5816", "description": "HONEYWELL SENSOR", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "5853", "processAs": "5853", "description": "HONEYWELL SENSOR (DO NOT PROCESS FG-1625 AS 5853)", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                
                # Brand/descriptor conversions
                {"original": "PROTECTION 1", "processAs": "2GIG-CP21-345E", "description": "ADT KEYPAD", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "tx id: 013-3285", "processAs": "2GIG-DW10-345", "description": "SMALL WINDOW/DOOR SENSOR", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                
                # Model number corrections
                {"original": "300-11260", "processAs": "300-10260", "description": "RESIDEO CLASS 2 POWER SUPPLY", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                {"original": "BP6024", "processAs": "60-670-95R", "description": "UL SENSORS", "notes": "", "disposition": "", "dateAdded": datetime.now().isoformat()},
                
                # ADT specific conversions
                {"original": "SA6150AS-VE", "processAs": "6150ADT", "description": "ADT KEYPAD", "notes": "", "disposition": "CR PROGRAM", "dateAdded": datetime.now().isoformat()},
                {"original": "SA6150RF-2", "processAs": "6150RF", "description": "HONEYWELL UL KEYPAD", "notes": "", "disposition": "SCRAP", "dateAdded": datetime.now().isoformat()},
                
                # Recent additions with default fallback
                {"original": "PG9933", "processAs": "OTHER SMOKE DETECTOR", "description": "DETECTOR", "notes": "ADDED 09/11", "disposition": "", "dateAdded": datetime.now().isoformat()},
            ]
            
            self._save_mappings(default_mappings)
    
    def _load_mappings(self) -> List[Dict[str, Any]]:
        """Load mappings from data file."""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.logger.warning(f"Could not load mappings: {e}")
            return []
    
    def _save_mappings(self, mappings: List[Dict[str, Any]]):
        """Save mappings to data file."""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(mappings, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Could not save mappings: {e}")
            raise
    
    def search_mappings(self, query: str) -> List[Dict[str, Any]]:
        """Search for part mappings based on query."""
        if not query or query.strip() == '':
            return []
        
        mappings = self._load_mappings()
        search_term = query.strip().upper()
        
        # Direct matches first
        exact_matches = [
            mapping for mapping in mappings 
            if mapping.get('original', '').upper() == search_term
        ]
        
        if exact_matches:
            return exact_matches
        
        # Partial matches
        partial_matches = [
            mapping for mapping in mappings 
            if (search_term in mapping.get('original', '').upper() or
                search_term in mapping.get('processAs', '').upper() or
                search_term in mapping.get('description', '').upper())
        ]
        
        return partial_matches[:10]  # Limit to 10 results
    
    def get_auto_conversion(self, input_part: str) -> Optional[Dict[str, Any]]:
        """Get automatic conversion for a part number."""
        if not input_part or input_part.strip() == '':
            return None
        
        mappings = self._load_mappings()
        search_term = input_part.strip().upper()
        
        # Look for exact match
        for mapping in mappings:
            if mapping.get('original', '').upper() == search_term:
                return mapping
        
        return None
    
    async def add_mapping(self, original: str, process_as: str, description: str, 
                         notes: str = '', disposition: str = '') -> Dict[str, Any]:
        """Add a new part mapping."""
        mappings = self._load_mappings()
        
        # Check if mapping already exists
        existing = next((m for m in mappings if m.get('original', '').upper() == original.upper()), None)
        if existing:
            raise ValueError(f"Mapping for '{original}' already exists")
        
        new_mapping = {
            'original': original.upper(),
            'processAs': process_as.upper(),
            'description': description,
            'notes': notes,
            'disposition': disposition.upper() if disposition else '',
            'dateAdded': datetime.now().isoformat(),
            'addedBy': 'system'  # Could be enhanced with user tracking
        }
        
        mappings.insert(0, new_mapping)  # Add to beginning
        self._save_mappings(mappings)
        
        self.logger.info(f"Added new part mapping: {original} -> {process_as}")
        return new_mapping
    
    def get_all_mappings(self) -> List[Dict[str, Any]]:
        """Get all part mappings."""
        return self._load_mappings()
    
    def get_mapping_stats(self) -> Dict[str, Any]:
        """Get statistics about part mappings."""
        mappings = self._load_mappings()
        
        # Calculate categories
        categories = {}
        dispositions = {}
        
        for mapping in mappings:
            # Categorize by description keywords
            desc = mapping.get('description', '').upper()
            if 'KEYPAD' in desc:
                categories['Keypads'] = categories.get('Keypads', 0) + 1
            elif 'CAMERA' in desc:
                categories['Cameras'] = categories.get('Cameras', 0) + 1
            elif 'SENSOR' in desc:
                categories['Sensors'] = categories.get('Sensors', 0) + 1
            elif 'ROUTER' in desc or 'WIFI' in desc:
                categories['Network'] = categories.get('Network', 0) + 1
            elif 'SMOKE' in desc or 'DETECTOR' in desc:
                categories['Detectors'] = categories.get('Detectors', 0) + 1
            elif 'LOCK' in desc:
                categories['Smart Locks'] = categories.get('Smart Locks', 0) + 1
            else:
                categories['Other'] = categories.get('Other', 0) + 1
            
            # Count dispositions
            disposition = mapping.get('disposition', '') or 'None'
            dispositions[disposition] = dispositions.get(disposition, 0) + 1
        
        return {
            'totalMappings': len(mappings),
            'categories': categories,
            'dispositions': dispositions,
            'lastUpdated': datetime.now().isoformat()
        }
    
    def update_mapping(self, original: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing mapping."""
        mappings = self._load_mappings()
        
        # Find the mapping to update
        for i, mapping in enumerate(mappings):
            if mapping.get('original', '').upper() == original.upper():
                # Update fields
                for key, value in updates.items():
                    if key in ['original', 'processAs', 'description', 'notes', 'disposition']:
                        mapping[key] = value
                
                mapping['lastModified'] = datetime.now().isoformat()
                mappings[i] = mapping
                
                self._save_mappings(mappings)
                self.logger.info(f"Updated mapping for: {original}")
                return mapping
        
        raise ValueError(f"Mapping for '{original}' not found")
    
    def delete_mapping(self, original: str) -> bool:
        """Delete a mapping."""
        mappings = self._load_mappings()
        
        # Find and remove the mapping
        original_count = len(mappings)
        mappings = [m for m in mappings if m.get('original', '').upper() != original.upper()]
        
        if len(mappings) < original_count:
            self._save_mappings(mappings)
            self.logger.info(f"Deleted mapping for: {original}")
            return True
        
        return False
