from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

class BaseAdapter(ABC):
    """Base adapter for any Python module integration"""
    
    @abstractmethod
    def initialize(self, **kwargs) -> None:
        """Initialize the adapter with configuration"""
        pass

    @abstractmethod
    def handle_data(self, data: Any) -> Any:
        """Process data in module-specific format"""
        pass

    @abstractmethod
    def serialize(self, data: Any) -> Dict:
        """Convert data to serializable format"""
        pass

    @abstractmethod
    def deserialize(self, data: Dict) -> Any:
        """Convert from serialized format to module-specific format"""
        pass
