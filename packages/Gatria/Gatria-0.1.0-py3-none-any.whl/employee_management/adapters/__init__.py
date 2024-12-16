from .base import BaseAdapter
from .module_adapters import WebAdapter, DBAdapter, AsyncAdapter, MLAdapter

class AdapterFactory:
    @staticmethod
    def create_adapter(module_type: str, specific_type: str) -> BaseAdapter:
        adapters = {
            'web': WebAdapter,
            'database': DBAdapter,
            'async': AsyncAdapter,
            'ml': MLAdapter
        }
        return adapters[module_type](specific_type)

__all__ = ['BaseAdapter', 'AdapterFactory', 'WebAdapter', 'DBAdapter', 'AsyncAdapter', 'MLAdapter']
