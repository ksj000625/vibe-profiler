import time
import random
from vibe_profiler import vibe_profile, show_vibe_report, get_optimization_prompt

print(">>> Starting Vibe Profiler Demo...\n")

@vibe_profile
def fast_but_frequent():
    """Example of a 'Good' vibe function (fast)."""
    # Simulate work < 1ms
    pass

@vibe_profile
def calculate_pi_inefficiently(n_terms: int):
    """Example of a 'Soso' or 'Bad' vibe function depending on n_terms."""
    pi = 0
    numerator = 4
    denominator = 1
    operator = 1
    
    for _ in range(n_terms):
        pi += operator * (numerator / denominator)
        denominator += 2
        operator *= -1
    return pi

@vibe_profile
def heavy_io_simulation():
    """Example of a 'Bad' vibe function (slow)."""
    time.sleep(0.12)  # 120ms
    return "Done"

# Run simulations
print("Running functions...")

# 1. Fast function called many times
for _ in range(50):
    fast_but_frequent()

# 2. Medium function
calculate_pi_inefficiently(1000)   # Fast enough
calculate_pi_inefficiently(50000)  # Roughly 10-20ms (Soso)

# 3. Slow function
heavy_io_simulation()

print("\n>>> Generating Vibe Report...\n")
show_vibe_report()

print("\n>>> Generating Optimization Prompt for 'heavy_io_simulation'...\n")
prompt = get_optimization_prompt("heavy_io_simulation")
print(prompt)
