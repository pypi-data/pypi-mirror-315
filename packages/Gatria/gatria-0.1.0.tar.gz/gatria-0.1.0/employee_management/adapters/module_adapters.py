from typing import Any, Dict, Optional
from .base import BaseAdapter
import json

class WebAdapter(BaseAdapter):
    def __init__(self, framework_type: str):
        self.framework_type = framework_type
        self.framework = None
        self.app = None

    def initialize(self, **kwargs):
        if self.framework_type == 'flask':
            from flask import Flask
            self.app = Flask(__name__)
            self.framework = self.app
        elif self.framework_type == 'django':
            from django.conf import settings
            self.framework = settings.configure(**kwargs)

    def serialize(self, data: Any) -> Dict:
        if isinstance(data, dict):
            return data
        elif hasattr(data, '__dict__'):
            return data.__dict__
        return {'data': str(data)}

    def deserialize(self, data: Dict) -> Any:
        return data

    def handle_data(self, data: Any) -> Any:
        serialized = self.serialize(data)
        if self.framework_type == 'flask':
            if not self.app:
                raise RuntimeError("Flask app not initialized")
            with self.app.app_context():
                from flask import jsonify
                return jsonify(serialized)
        return serialized

class DBAdapter(BaseAdapter):
    def __init__(self, db_type: str):
        self.db_type = db_type
        self.connection = None

    def initialize(self, **kwargs):
        if self.db_type == 'sqlalchemy':
            from sqlalchemy import create_engine
            self.connection = create_engine(kwargs['connection_string'])
        elif self.db_type == 'mongodb':
            from pymongo import MongoClient
            self.connection = MongoClient(kwargs['connection_string'])

    def serialize(self, data: Any) -> Dict:
        if isinstance(data, dict):
            return data
        return {'data': str(data)}

    def deserialize(self, data: Dict) -> Any:
        return data

    def handle_data(self, data: Any) -> Any:
        return self.serialize(data)

class AsyncAdapter(BaseAdapter):
    def __init__(self, framework_type: str):
        self.framework_type = framework_type
        
    def initialize(self, **kwargs):
        if self.framework_type == 'asyncio':
            import asyncio
            self.loop = asyncio.get_event_loop()
        elif self.framework_type == 'aiohttp':
            import aiohttp
            self.session = aiohttp.ClientSession()

    def serialize(self, data: Any) -> Dict:
        if isinstance(data, dict):
            return data
        return {'data': str(data)}

    def deserialize(self, data: Dict) -> Any:
        return data

    async def handle_data(self, data: Any) -> Any:
        return self.serialize(data)

class MLAdapter(BaseAdapter):
    def __init__(self, framework_type: str):
        self.framework_type = framework_type
        
    def initialize(self, **kwargs):
        if self.framework_type == 'sklearn':
            import sklearn
            self.framework = sklearn
        elif self.framework_type == 'tensorflow':
            import tensorflow as tf
            self.framework = tf

    def serialize(self, data: Any) -> Dict:
        if isinstance(data, dict):
            return data
        import numpy as np
        if isinstance(data, np.ndarray):
            return {'data': data.tolist()}
        return {'data': str(data)}

    def deserialize(self, data: Dict) -> Any:
        return data

    def handle_data(self, data: Any) -> Any:
        return self.serialize(data)
