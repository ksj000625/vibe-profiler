import argparse
from .profiler import VibeProfiler

def main():
    parser = argparse.ArgumentParser(
        description="Vibe Profiler CLI — measure and display friendly speed levels ⚡🐢"
    )

    parser.add_argument(
        "command",
        choices=["report", "clear"],
        help="Command to execute (report, clear)",
    )

    args = parser.parse_args()
    profiler = VibeProfiler()

    if args.command == "report":
        profiler.report()
    elif args.command == "clear":
        profiler.records.clear()
        print("Profiler data cleared.")
