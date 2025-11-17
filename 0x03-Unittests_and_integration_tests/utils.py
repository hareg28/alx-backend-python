#!/usr/bin/env python3
"""Utils module for unit and integration testing"""

from typing import Any, Dict, Tuple, Callable
import requests
from functools import wraps

def access_nested_map(nested_map: Dict, path: Tuple) -> Any:
    """Access a nested map using a sequence of keys"""
    current = nested_map
    for key in path:
        current = current[key]
    return current

def get_json(url: str) -> Dict:
    """Get JSON content from a URL"""
    response = requests.get(url)
    return response.json()

def memoize(fn: Callable) -> Callable:
    """Decorator to memoize instance method results"""
    attr_name = f"_memoized_{fn.__name__}"

    @property
    @wraps(fn)
    def wrapper(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)
    return wrapper
