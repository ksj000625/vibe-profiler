import os
import time
from vibe_profiler import vibe_profile, show_vibe_report, OpenAIEngine

# Check for API Key
if "OPENAI_API_KEY" not in os.environ:
    print("Please set OPENAI_API_KEY environment variable to run this demo.")
    print("export OPENAI_API_KEY='sk-...'")
    exit(1)

print(">>> Starting Vibe Profiler with OpenAI Engine...\n")

@vibe_profile
def inefficient_list_creation():
    """Creates a list in a very inefficient way."""
    result = []
    for i in range(10000):
        result.insert(0, i)  # O(n) insertion at start
    return result

print("Running function...")
inefficient_list_creation()

print("\n>>> Generating Vibe Report (Consulting OpenAI)...\n")
# Initialize the engine with the API key from env
engine = OpenAIEngine()

# Pass the engine to the reporter
show_vibe_report(ai_engine=engine)
