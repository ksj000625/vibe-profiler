from functools import wraps
import time

def vibe_profile(profiler):
    """
    vibe_profile decorator
    -----------------------
    Measures the execution time of a function and records it in the VibeProfiler instance.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            end = time.perf_counter()

            duration_ms = (end - start) * 1000
            profiler.record(func.__name__, duration_ms)
            return result

        return wrapper
    return decorator
