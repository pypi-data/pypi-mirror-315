from typing import Any, Dict, Optional

class JSONResponse:
    def __init__(
        self, 
        data: Any = None, 
        status_code: int = 200, 
        message: str = "",
        success: bool = True
    ):
        self.data = data
        self.status_code = status_code
        self.message = message
        self.success = success

    def to_dict(self) -> Dict:
        return {
            "success": self.success,
            "message": self.message,
            "data": self.data,
            "status_code": self.status_code
        }

class APIResponse(JSONResponse):
    def __init__(
        self,
        data: Any = None,
        status_code: int = 200,
        message: str = "",
        metadata: Optional[Dict] = None
    ):
        super().__init__(data, status_code, message)
        self.metadata = metadata or {}

    def to_dict(self) -> Dict:
        response = super().to_dict()
        response["metadata"] = self.metadata
        return response
