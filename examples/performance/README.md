# Performance & Benchmark Examples

Examples for performance testing and benchmarking with Goal.

## Benchmarking Commit Generation

```python
# benchmark_commit.py
"""Benchmark commit message generation performance."""

import time
import statistics
from goal.push.stages import get_commit_message

def benchmark_commit_generation(iterations=100):
    """Benchmark commit generation performance."""
    
    # Test data
    files = [f"src/module{i}.py" for i in range(50)]
    diff = generate_large_diff()  # Helper to create realistic diff
    
    ctx_obj = {'yes': True, 'markdown': False}
    
    times = []
    
    for _ in range(iterations):
        start = time.perf_counter()
        
        title, body, result = get_commit_message(
            ctx_obj, files, diff, message=None, ticket=None, abstraction=None
        )
        
        elapsed = time.perf_counter() - start
        times.append(elapsed)
    
    # Statistics
    avg_time = statistics.mean(times)
    median_time = statistics.median(times)
    stdev_time = statistics.stdev(times)
    
    print(f"Commit Generation Benchmark ({iterations} iterations):")
    print(f"  Average: {avg_time*1000:.2f}ms")
    print(f"  Median:  {median_time*1000:.2f}ms")
    print(f"  Std Dev: {stdev_time*1000:.2f}ms")
    print(f"  Min:     {min(times)*1000:.2f}ms")
    print(f"  Max:     {max(times)*1000:.2f}ms")

if __name__ == "__main__":
    benchmark_commit_generation()
```

## Profiling Goal Commands

```python
# profile_goal.py
"""Profile Goal command execution."""

import cProfile
import pstats
import io
from contextlib import contextmanager

@contextmanager
def profile_execution(sort_by='cumulative', lines=20):
    """Context manager for profiling code blocks."""
    profiler = cProfile.Profile()
    profiler.enable()
    
    try:
        yield
    finally:
        profiler.disable()
        
        # Print stats
        stream = io.StringIO()
        stats = pstats.Stats(profiler, stream=stream)
        stats.sort_stats(sort_by)
        stats.print_stats(lines)
        
        print(stream.getvalue())

# Usage
def test_profiled():
    with profile_execution():
        # Run your Goal code
        from goal.push.core import execute_push_workflow
        # ... your test code ...
        pass
```

## Memory Usage Tracking

```python
# memory_benchmark.py
"""Track memory usage during Goal operations."""

import tracemalloc
import sys
from contextlib import contextmanager

@contextmanager
def track_memory():
    """Context manager to track peak memory usage."""
    tracemalloc.start()
    
    try:
        yield
    finally:
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        print(f"Current memory: {current / 1024 / 1024:.2f} MB")
        print(f"Peak memory: {peak / 1024 / 1024:.2f} MB")

# Usage in tests
def test_memory_usage():
    with track_memory():
        # Run memory-intensive Goal operation
        from goal.project_bootstrap import bootstrap_all_projects
        bootstrap_all_projects()
```

## Large Repository Testing

```python
# large_repo_test.py
"""Test Goal performance with large repositories."""

import tempfile
from pathlib import Path
import subprocess

def create_large_repo(num_commits=1000, num_files=100):
    """Create test repository with many commits."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo = Path(tmpdir)
        
        # Initialize
        subprocess.run(['git', 'init'], cwd=repo, capture_output=True)
        
        # Create many files and commits
        for i in range(num_commits):
            # Modify files
            for j in range(num_files):
                file_path = repo / f"file{j}.txt"
                file_path.write_text(f"Content {i}-{j}\n")
            
            # Commit
            subprocess.run(['git', 'add', '.'], cwd=repo, capture_output=True)
            subprocess.run(
                ['git', 'commit', '-m', f"Commit {i}"],
                cwd=repo, capture_output=True
            )
        
        return repo

def benchmark_large_repo():
    """Benchmark Goal operations on large repo."""
    import time
    
    repo = create_large_repo(num_commits=500, num_files=50)
    
    # Benchmark git operations
    from goal.git_ops import get_staged_files, get_diff_stats
    
    start = time.perf_counter()
    files = get_staged_files()
    elapsed = time.perf_counter() - start
    print(f"get_staged_files: {elapsed*1000:.2f}ms")
    
    # Benchmark commit generation
    from goal.push.stages import get_commit_message
    
    ctx_obj = {'yes': True}
    diff = "mock diff content"
    
    start = time.perf_counter()
    get_commit_message(ctx_obj, files, diff, None, None, None)
    elapsed = time.perf_counter() - start
    print(f"get_commit_message: {elapsed*1000:.2f}ms")
```

## Parallel Execution Benchmark

```python
# parallel_benchmark.py
"""Benchmark parallel vs sequential execution."""

import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import multiprocessing

def benchmark_sequential(tasks):
    """Run tasks sequentially."""
    start = time.perf_counter()
    results = [task() for task in tasks]
    elapsed = time.perf_counter() - start
    return elapsed, results

def benchmark_threaded(tasks, max_workers=4):
    """Run tasks with thread pool."""
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(lambda f: f(), tasks))
    elapsed = time.perf_counter() - start
    return elapsed, results

def benchmark_multiprocess(tasks, max_workers=4):
    """Run tasks with process pool."""
    start = time.perf_counter()
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(lambda f: f(), tasks))
    elapsed = time.perf_counter() - start
    return elapsed, results

# Example usage with Goal
def test_parallel_validation():
    """Test parallel file validation."""
    from goal.validators import validate_staged_files
    
    def validation_task():
        return validate_staged_files(None)
    
    tasks = [validation_task for _ in range(10)]
    
    seq_time, _ = benchmark_sequential(tasks)
    thread_time, _ = benchmark_threaded(tasks)
    
    print(f"Sequential: {seq_time:.2f}s")
    print(f"Threaded:   {thread_time:.2f}s")
    print(f"Speedup:    {seq_time/thread_time:.2f}x")
```

## Configuration for Performance

```yaml
# goal.yaml for performance
version: "1.0"

project:
  name: "performance-optimized"

advanced:
  performance:
    # Parallel processing
    parallel_tests: true
    max_workers: 4
    
    # Caching
    cache_enabled: true
    cache_ttl: 3600
    
    # Timeouts
    max_commit_time: 30
    max_test_time: 300
    max_publish_time: 600
    
    # Resource limits
    max_memory_mb: 2048
    max_file_size_mb: 50
```

## Performance Monitoring

```python
# monitoring.py
"""Monitor Goal performance in production."""

import time
import functools
import logging

logger = logging.getLogger('goal.performance')

def timed(func):
    """Decorator to time function execution."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        
        logger.info(f"{func.__name__}: {elapsed*1000:.2f}ms")
        
        # Alert if too slow
        if elapsed > 5:  # 5 seconds
            logger.warning(f"{func.__name__} took {elapsed:.2f}s")
        
        return result
    return wrapper

# Usage
from goal.push.stages import get_commit_message as original_get_message

get_commit_message = timed(original_get_message)
```

## Running Benchmarks

```bash
# Install pytest-benchmark
pip install pytest-benchmark

# Run benchmarks
pytest benchmark_commit.py --benchmark-only

# Compare runs
pytest benchmark_commit.py --benchmark-compare

# Save results
pytest benchmark_commit.py --benchmark-json=results.json

# Generate histogram
pytest benchmark_commit.py --benchmark-histogram=hist
```

## See Also

- [Testing Guide](../testing-guide/)
- [CI/CD Optimization](../../docs/ci-cd.md)
