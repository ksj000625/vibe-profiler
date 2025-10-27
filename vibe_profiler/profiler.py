from collections import defaultdict
from statistics import mean
from .resources import ResourceMonitor
from .code_analyzer import CodeAnalyzer

class VibeProfiler:
    """
    A profiler that collects function execution time, memory usage, and I/O usage.
    Also detects common inefficient patterns in the analyzed functions.
    """
    def __init__(self):
        self.records = defaultdict(list)
        self.resource_monitor = ResourceMonitor()
        self.code_analyzer = CodeAnalyzer()
        self.function_warnings = {}

    def record(self, func_name: str, stats: dict, func_ref=None):
        """Store the profiling result of a function and analyze its code."""
        self.records[func_name].append(stats)
        if func_ref and func_name not in self.function_warnings:
            self.function_warnings[func_name] = self.code_analyzer.analyze(func_ref)

    def get_level(self, avg_ms: float) -> str:
        """Vibe-coder-friendly speed rating."""
        if avg_ms < 100:
            return "Fast ⚡"
        elif avg_ms < 250:
            return "Normal 🙂"
        else:
            return "Slow 🐢"

    def report(self):
        """Display profiling results in CLI format."""
        print("\n================ Vibe Profiler Report ================")
        print(f"{'Function Name':<20} {'Avg (ms)':<10} {'Mem(KB)':<10} {'I/O(KB)':<10} {'Level':<8}")
        print("-" * 75)

        for func_name, entries in self.records.items():
            avg_ms = mean(e["duration_ms"] for e in entries)
            avg_mem = mean(e["memory_used"] for e in entries) / 1024
            avg_io = mean(e["io_read_diff"] + e["io_write_diff"] for e in entries) / 1024
            level = self.get_level(avg_ms)
            print(f"{func_name:<20} {avg_ms:<10.1f} {avg_mem:<10.1f} {avg_io:<10.1f} {level}")

            # 🔍 show detected code warnings
            if func_name in self.function_warnings:
                for warn in self.function_warnings[func_name]:
                    print(f"   {warn}")

        print("-" * 75)
        print("Speed Guide: Fast < 100ms < Normal < 250ms < Slow")
        print("=" * 75)
