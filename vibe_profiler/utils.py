import time
from functools import wraps

def vibe_profile(profiler):
    """
    A decorator that automatically measures performance and resource usage before and after function execution.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            monitor = profiler.resource_monitor
            monitor.start()

            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()

            duration_ms = (end - start) * 1000
            resource_stats = monitor.stop()
            resource_stats["duration_ms"] = duration_ms

            profiler.record(func.__name__, resource_stats)
            return result
        return wrapper
    return decorator
