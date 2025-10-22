from vibe_profiler import vibe_profile, VibeProfiler
import time

profiler = VibeProfiler()

@vibe_profile(profiler)
def slow_function():
    time.sleep(0.3)

@vibe_profile(profiler)
def fast_function():
    time.sleep(0.02)

if __name__ == "__main__":
    for _ in range(3):
        slow_function()
        fast_function()

    profiler.report()
