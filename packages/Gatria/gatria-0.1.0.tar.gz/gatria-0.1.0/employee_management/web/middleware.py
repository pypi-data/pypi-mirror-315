from typing import Callable, Any

class AuthMiddleware:
    def __init__(self, app: Any):
        self.app = app

    def __call__(self, *args, **kwargs):
        # Basic authentication middleware
        return self.app(*args, **kwargs)

class CORSMiddleware:
    def __init__(self, app: Any):
        self.app = app

    def __call__(self, *args, **kwargs):
        # Basic CORS middleware
        return self.app(*args, **kwargs)
