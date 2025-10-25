from vibe_profiler import VibeProfiler, vibe_profile
import time, requests

profiler = VibeProfiler()

@vibe_profile(profiler)
def compute_heavy():
    sum(i**2 for i in range(1_000_000))

@vibe_profile(profiler)
def io_heavy():
    requests.get("https://example.com")

@vibe_profile(profiler)
def sleep_slow():
    time.sleep(0.3)

if __name__ == "__main__":
    compute_heavy()
    io_heavy()
    sleep_slow()
    profiler.report()
