from rich import print
from rich.console import Console
from rich.table import Table
from typing import Optional
from .profiler import get_all_stats
from .ai_engine import AIEngine, SimpleHeuristicEngine

class VibeReporter:
    def __init__(self, ai_engine: Optional[AIEngine] = None):
        if ai_engine is None:
            self.ai_engine = SimpleHeuristicEngine()
        else:
            self.ai_engine = ai_engine
        
        self.console = Console()

    def show_report(self):
        stats = get_all_stats()
        if not stats:
            self.console.print("[yellow]No execution data found to report.[/yellow]")
            return

        table = Table(title="Vibe Profiler Report", show_header=True, header_style="bold magenta")
        table.add_column("Function Name", style="cyan")
        table.add_column("Calls", justify="right")
        table.add_column("Avg Time (ms)", justify="right")
        table.add_column("Vibe Level", justify="center")
        table.add_column("Advice", style="green")

        for stat in stats:
            avg_time = stat.avg_time_ms
            rating = self.ai_engine.get_vibe_rating(stat.name, avg_time, stat.source_code)
            advice = self.ai_engine.get_optimization_advice(stat.name, avg_time, stat.source_code)
            
            # Color code the rating
            rating_style = ""
            if rating == "Bad":
                rating_style = "bold red"
            elif rating == "Soso":
                rating_style = "yellow"
            else:
                rating_style = "bold green"
            
            table.add_row(
                stat.name,
                str(stat.call_count),
                f"{avg_time:.4f}",
                f"[{rating_style}]{rating}[/{rating_style}]",
                advice
            )

        self.console.print(table)

    def generate_prompt(self, func_name: str) -> str:
        stats = get_all_stats()
        target_stat = next((s for s in stats if s.name == func_name), None)
        
        if not target_stat:
            return f"Function '{func_name}' not found in registry."
            
        return self.ai_engine.generate_optimization_prompt(
            target_stat.name, 
            target_stat.avg_time_ms, 
            target_stat.source_code
        )

# Convenience function
def show_vibe_report(ai_engine: Optional[AIEngine] = None):
    reporter = VibeReporter(ai_engine)
    reporter.show_report()

def get_optimization_prompt(func_name: str, ai_engine: Optional[AIEngine] = None) -> str:
    reporter = VibeReporter(ai_engine)
    return reporter.generate_prompt(func_name)
