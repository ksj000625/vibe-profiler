import psutil
import time

class ResourceMonitor:
    """
    ResourceMonitor
    ----------------
    Measures CPU, memory, and I/O blocking time during function execution.
    """

    def __init__(self):
        self.process = psutil.Process()
        self.start_memory = 0
        self.start_io = None
        self.start_time = 0

    def start(self):
        """Start measurement."""
        self.start_memory = self.process.memory_info().rss
        self.start_time = time.time()
        self.start_io = getattr(self.process, "io_counters", lambda: None)()

    def stop(self):
        """Stop measurement and return results."""
        end_time = time.time()
        elapsed_time = (end_time - self.start_time) * 1000  # ms

        end_memory = self.process.memory_info().rss
        mem_diff = end_memory - self.start_memory

        end_io = getattr(self.process, "io_counters", lambda: None)()
        io_read_diff, io_write_diff = 0, 0
        if self.start_io and end_io:
            io_read_diff = end_io.read_bytes - self.start_io.read_bytes
            io_write_diff = end_io.write_bytes - self.start_io.write_bytes

        return {
            "duration_ms": round(elapsed_time, 2),
            "memory_used": mem_diff,
            "io_read_diff": io_read_diff,
            "io_write_diff": io_write_diff
        }
