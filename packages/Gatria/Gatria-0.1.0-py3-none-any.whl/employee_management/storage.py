import json
import os
from typing import Any, Dict
from datetime import datetime
from enum import Enum

class StorageManager:
    @staticmethod
    def save_data(filepath: str, data: Dict) -> bool:
        """Safely save data to JSON file with backup"""
        try:
            # Create backup of existing file
            if os.path.exists(filepath):
                backup_path = f"{filepath}.backup"
                os.replace(filepath, backup_path)

            # Convert datetime objects to ISO format
            serializable_data = StorageManager._prepare_for_serialization(data)

            # Write new data
            with open(filepath, 'w') as f:
                json.dump(serializable_data, f, indent=4)

            return True

        except Exception as e:
            # Restore from backup if save failed
            if os.path.exists(f"{filepath}.backup"):
                os.replace(f"{filepath}.backup", filepath)
            raise RuntimeError(f"Failed to save data: {str(e)}")  # Fixed missing quote

    @staticmethod
    def load_data(filepath: str, default_value: Any = None) -> Dict:
        """Safely load data from JSON file"""
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    return json.load(f)
            return default_value or {}

        except Exception as e:
            # Try loading from backup if main file is corrupted
            backup_path = f"{filepath}.backup"
            if os.path.exists(backup_path):
                with open(backup_path, 'r') as f:
                    return json.load(f)
            return default_value or {}

    @staticmethod
    def _prepare_for_serialization(data: Dict) -> Dict:
        """Convert data types to JSON-serializable format"""
        if isinstance(data, dict):
            return {k: StorageManager._prepare_for_serialization(v) 
                   for k, v in data.items()}
        elif isinstance(data, list):
            return [StorageManager._prepare_for_serialization(v) for v in data]
        elif isinstance(data, datetime):
            return data.isoformat()
        elif isinstance(data, Enum):
            return data.value
        return data
