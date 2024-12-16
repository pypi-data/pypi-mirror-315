import os
from dataclasses import dataclass
from typing import Dict
import json
import logging

@dataclass
class SystemConfig:
    max_leave_days: int = 30
    min_performance_rating: float = 1.0
    max_performance_rating: float = 5.0
    attendance_grace_period_minutes: int = 15
    data_storage_path: str = "data"

class ConfigManager:
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.config = SystemConfig()
        self._initialize_system()
        self._load_config()

    def _initialize_system(self):
        """Initialize required directories and files"""
        # Create data directory if it doesn't exist
        os.makedirs(self.config.data_storage_path, exist_ok=True)
        
        # Create default config if it doesn't exist
        if not os.path.exists(self.config_file):
            self._create_default_config()

    def _create_default_config(self):
        """Create default configuration file"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config.__dict__, f, indent=4)

    def get_storage_path(self, filename: str) -> str:
        """Get full path for a storage file"""
        return os.path.join(self.config.data_storage_path, filename)

    def _load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                config_data = json.load(f)
                self.config = SystemConfig(**config_data)
