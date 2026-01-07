from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import os

class AIEngine(ABC):
    """Abstract base class for Vibe Check AI Engines."""

    @abstractmethod
    def get_vibe_rating(self, func_name: str, avg_time_ms: float, source_code: str) -> str:
        """
        Analyze the function performance and code to return a Vibe rating.
        Expected return values: 'Bad', 'Soso', 'Good'.
        """
        pass

    @abstractmethod
    def get_optimization_advice(self, func_name: str, avg_time_ms: float, source_code: str) -> str:
        """
        Generate optimization advice or a prompt for the user.
        """
        pass
    
    @abstractmethod
    def generate_optimization_prompt(self, func_name: str, avg_time_ms: float, source_code: str) -> str:
        """
        Generates a specific prompt used for the AI or user.
        """
        pass


class SimpleHeuristicEngine(AIEngine):
    """
    A simple MVP engine that uses execution time thresholds 
    instead of calling an actual AI API.
    """

    def __init__(self, bad_threshold_ms: float = 100.0, soso_threshold_ms: float = 10.0):
        self.bad_threshold_ms = bad_threshold_ms
        self.soso_threshold_ms = soso_threshold_ms

    def get_vibe_rating(self, func_name: str, avg_time_ms: float, source_code: str) -> str:
        if avg_time_ms >= self.bad_threshold_ms:
            return "Bad"
        elif avg_time_ms >= self.soso_threshold_ms:
            return "Soso"
        else:
            return "Good"

    def get_optimization_advice(self, func_name: str, avg_time_ms: float, source_code: str) -> str:
        rating = self.get_vibe_rating(func_name, avg_time_ms, source_code)
        
        if rating == "Bad":
            return (
                f"OMFG, {func_name} is taking {avg_time_ms:.2f}ms! "
                "This is too slow. Consider optimizing loops or I/O."
            )
        elif rating == "Soso":
            return (
                f"{func_name} is okay ({avg_time_ms:.2f}ms), but could be snappier. "
                "Check for minor inefficiencies."
            )
        else:
            return "Slay! Pure speed."

    def generate_optimization_prompt(self, func_name: str, avg_time_ms: float, source_code: str) -> str:
        """
        Generates a specific prompt that the user can copy-paste to an LLM 
        to get actual code improvements.
        """
        return f"""
You are a Python performance expert. 
The function `{func_name}` is currently performing poorly with an average execution time of {avg_time_ms:.2f}ms.
Here is the source code:

```python
{source_code}
```

Please analyze why this might be slow and provide an optimized version of the code that maintains the same functionality but improves performance.
"""

class OpenAIEngine(AIEngine):
    """
    AI Engine that uses OpenAI API to analyze function performance.
    """
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o"):
        try:
            import openai
        except ImportError:
            raise ImportError("openai package is required for OpenAIEngine. Run `pip install openai`.")
            
        self.client = openai.OpenAI(api_key=api_key or os.environ.get("OPENAI_API_KEY"))
        self.model = model

    def get_vibe_rating(self, func_name: str, avg_time_ms: float, source_code: str) -> str:
        # Fallback to heuristics if code is too long or simple to avoid latency/cost on every check
        # But per requirements we try to use AI.
        # Let's use a very short prompt to get classification.
        
        prompt = f"""
        Function: {func_name}
        Avg Time: {avg_time_ms:.2f}ms
        Code:
        {source_code[:1000]}... (truncated)

        Rate performance as one of: Bad, Soso, Good. 
        Context: 'Bad' is practically unusable or very slow. 'Soso' is acceptable but improvable. 'Good' is optimal.
        Reply ONLY with the word.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=10
            )
            content = response.choices[0].message.content.strip()
            if content in ["Bad", "Soso", "Good"]:
                return content
            return "Soso" # Default fallback
        except Exception:
            return "Soso" # Fallback on error

    def get_optimization_advice(self, func_name: str, avg_time_ms: float, source_code: str) -> str:
        prompt = f"""
        Function: {func_name}
        Avg Time: {avg_time_ms:.2f}ms
        Code:
        {source_code[:2000]}

        Give a very pithy, 1-sentence vibe check/advice on this performance. Be witty.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=60
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"AI Error: {str(e)}"

    def generate_optimization_prompt(self, func_name: str, avg_time_ms: float, source_code: str) -> str:
        # For OpenAI engine, we can actually just ask the AI to generate the optimized code directly
        # But to keep interface consistent, we returns the prompt we WOULD send, or result?
        # The requirement says "returns the Optimization Prompt string".
        # If the user wants to copy paste this to ChatGPT, we return the prompt text.
        
        return f"""
You are a Python performance expert. 
The function `{func_name}` is currently performing with an average execution time of {avg_time_ms:.2f}ms.
Here is the source code:

```python
{source_code}
```

Please analyze why this might be slow and provide an optimized version of the code that maintains the same functionality but improves performance.
"""
