from abc import ABC, abstractmethod
from typing import Any, Dict
from .responses import JSONResponse, APIResponse

class WebFrameworkAdapter(ABC):
    @abstractmethod
    def create_response(self, data: Any, status_code: int = 200) -> Any:
        pass

    @abstractmethod
    def get_request_data(self) -> Dict:
        pass

class FlaskAdapter(WebFrameworkAdapter):
    def create_response(self, data: Any, status_code: int = 200) -> Any:
        from flask import jsonify
        response = JSONResponse(data=data, status_code=status_code)
        return jsonify(response.to_dict()), status_code

    def get_request_data(self) -> Dict:
        from flask import request
        return request.get_json()

class DjangoAdapter(WebFrameworkAdapter):
    def create_response(self, data: Any, status_code: int = 200) -> Any:
        from django.http import JsonResponse
        response = APIResponse(data=data, status_code=status_code)
        return JsonResponse(response.to_dict(), status=status_code)

    def get_request_data(self) -> Dict:
        from django.http import HttpRequest
        return self.request.POST or self.request.GET
