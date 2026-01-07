import functools
import time
import inspect
from typing import Dict, Any, List
from dataclasses import dataclass, field

@dataclass
class FunctionStats:
    name: str
    call_count: int = 0
    total_time_us: float = 0.0
    source_code: str = ""
    
    @property
    def avg_time_ms(self) -> float:
        if self.call_count == 0:
            return 0.0
        # Convert total microseconds to average milliseconds
        return (self.total_time_us / self.call_count) / 1000.0

class ProfilerRegistry:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ProfilerRegistry, cls).__new__(cls)
            cls._instance.stats = {}
        return cls._instance
    
    def __init__(self):
        # Prevent re-initialization if already created
        if not hasattr(self, 'stats'):
            self.stats: Dict[str, FunctionStats] = {}
            
    def register(self, func_name: str, execution_time_us: float, source_code: str = ""):
        if func_name not in self.stats:
            self.stats[func_name] = FunctionStats(name=func_name, source_code=source_code)
        
        stat = self.stats[func_name]
        stat.call_count += 1
        stat.total_time_us += execution_time_us
        if not stat.source_code and source_code:
            stat.source_code = source_code

    def get_stats(self) -> List[FunctionStats]:
        return list(self.stats.values())

    def clear(self):
        self.stats.clear()

# Global registry instance
_registry = ProfilerRegistry()

def vibe_profile(func):
    """
    Decorator to measure execution time of a function.
    Stores stats in the global ProfilerRegistry.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Capture source code once
        try:
            source_code = inspect.getsource(func)
        except OSError:
            source_code = "Source code not available"

        start_time = time.perf_counter()
        try:
            result = func(*args, **kwargs)
        finally:
            end_time = time.perf_counter()
            # Convert to microseconds for better precision on fast functions
            elapsed_us = (end_time - start_time) * 1_000_000
            
            _registry.register(func.__name__, elapsed_us, source_code)
            
        return result
    return wrapper

def get_all_stats() -> List[FunctionStats]:
    return _registry.get_stats()

def clear_stats():
    _registry.clear()
