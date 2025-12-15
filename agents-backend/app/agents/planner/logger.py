# planner/logger.py
import time
import logging

logging.basicConfig(level=logging.INFO)

def log_step(agent: str, task: str):
    logging.info(f"[{agent}] → {task}")

def timeit(fn):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = fn(*args, **kwargs)
        duration = (time.perf_counter() - start) * 1000
        return result, duration
    return wrapper
