from abc import ABC, abstractmethod
from typing import Dict, Any, List
from datetime import datetime

class IStorageAdapter(ABC):
    @abstractmethod
    def save(self, key: str, data: Dict) -> bool:
        pass

    @abstractmethod
    def load(self, key: str) -> Dict:
        pass

class IAuthenticationAdapter(ABC):
    @abstractmethod
    def authenticate(self, credentials: Dict) -> bool:
        pass

    @abstractmethod
    def authorize(self, user_id: str, action: str) -> bool:
        pass

class IAPIResponse:
    def __init__(self, success: bool, data: Any = None, error: str = None):
        self.success = success
        self.data = data
        self.error = error
        self.timestamp = datetime.now().isoformat()

    def to_dict(self) -> Dict:
        return {
            "success": self.success,
            "data": self.data,
            "error": self.error,
            "timestamp": self.timestamp
        }
