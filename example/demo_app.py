from vibe_profiler import VibeProfiler, vibe_profile
import requests, time

profiler = VibeProfiler()

@vibe_profile(profiler)
def bad_example():
    for _ in range(3):
        with open("temp.txt", "w") as f:
            f.write("hello")  # ❌ File I/O in loop
        requests.get("https://example.com")  # ❌ network call in loop

@vibe_profile(profiler)
def good_example():
    data = [i**2 for i in range(1000)]
    return sum(data)

if __name__ == "__main__":
    bad_example()
    good_example()
    profiler.report()
