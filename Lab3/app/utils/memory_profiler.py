import tracemalloc
from contextlib import contextmanager


@contextmanager
def track_memory_peak():
    """Контекстный менеджер для замера пикового потребления памяти."""
    tracemalloc.start()
    try:
        yield
    finally:
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        print(f"Peak memory usage: {peak / 1024 / 1024:.2f} MB")
