import time
from collections import defaultdict
from statistics import mean

class VibeProfiler:
    def __init__(self):
        self.records = defaultdict(list)

    def record(self, func_name, duration_ms):
        self.records[func_name].append(duration_ms)

    def get_level(self, avg_ms):
        if avg_ms < 100:
            return "Fast ⚡"
        elif avg_ms < 250:
            return "Normal 🙂"
        else:
            return "Slow 🐢"

    def report(self):
        print("\n================ Vibe Profiler Report ================")
        print(f"{'Function Name':<20} {'Avg (ms)':<10} {'Count':<7} Level")
        print("-" * 55)

        for func_name, times in self.records.items():
            avg_ms = mean(times)
            level = self.get_level(avg_ms)
            print(f"{func_name:<20} {avg_ms:<10.1f} {len(times):<7} {level}")

        print("-" * 55)
        print("Speed Guide: Fast < 100ms < Normal < 250ms < Slow")
        print("=" * 55)
