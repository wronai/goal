#!/usr/bin/env python3
"""
Run all examples in the examples directory.

This script runs all runnable Python examples and reports results.
"""

import subprocess
import sys
from pathlib import Path
from typing import List, Tuple
import time


class ExampleRunner:
    """Runs all examples and collects results."""
    
    def __init__(self, examples_dir: Path):
        self.examples_dir = examples_dir
        self.results: List[Tuple[str, bool, str, float]] = []
        
    def run_python_file(self, file_path: Path) -> Tuple[bool, str]:
        """Run a single Python file."""
        try:
            # Run with timeout
            result = subprocess.run(
                [sys.executable, str(file_path)],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=str(file_path.parent)
            )
            
            if result.returncode == 0:
                return True, "SUCCESS"
            else:
                # Truncate long error messages
                err = result.stderr[:200] if result.stderr else "Exit code != 0"
                return False, err
                
        except subprocess.TimeoutExpired:
            return False, "TIMEOUT (30s)"
        except Exception as e:
            return False, str(e)[:100]
    
    def run_all(self):
        """Find and run all Python examples."""
        # Categorize examples by their requirements
        self.simple_examples = []  # Can run standalone
        self.env_examples = []     # Need environment variables
        self.arg_examples = []     # Need command line arguments
        self.hook_examples = []    # Need git context
        
        # Scan directories
        scan_dirs = [
            ('api-usage', self.simple_examples),
            ('testing', self.simple_examples),
            ('performance', self.simple_examples),
            ('webhooks', self.env_examples),  # Need env vars
            ('custom-hooks', self.hook_examples),  # Git hooks
            ('template-generator', self.arg_examples),  # Needs args
        ]
        
        for subdir, target_list in scan_dirs:
            subdir_path = self.examples_dir / subdir
            if subdir_path.exists():
                for py_file in subdir_path.rglob("*.py"):
                    if '__pycache__' in str(py_file):
                        continue
                    if py_file.name == 'run_all_examples.py':
                        continue
                    target_list.append(py_file)
        
        total = len(self.simple_examples) + len(self.env_examples) + len(self.hook_examples) + len(self.arg_examples)
        print(f"Found {total} examples:")
        print(f"  - Simple (standalone): {len(self.simple_examples)}")
        print(f"  - Environment vars needed: {len(self.env_examples)}")
        print(f"  - Git hooks (special context): {len(self.hook_examples)}")
        print(f"  - Arguments needed: {len(self.arg_examples)}")
        print()
        
        # Run simple examples
        print("Running standalone examples:")
        for file_path in sorted(self.simple_examples):
            self._run_example(file_path)
        
        # Skip env-dependent with warning
        if self.env_examples:
            print(f"\nSkipping {len(self.env_examples)} examples (need environment variables):")
            for file_path in sorted(self.env_examples):
                rel_path = file_path.relative_to(self.examples_dir)
                print(f"  ⚠️  {rel_path} (needs env vars)")
                self.results.append((str(rel_path), False, "SKIP: needs env vars", 0))
        
        # Skip hooks with warning  
        if self.hook_examples:
            print(f"\nSkipping {len(self.hook_examples)} examples (git hooks):")
            for file_path in sorted(self.hook_examples):
                rel_path = file_path.relative_to(self.examples_dir)
                print(f"  ⚠️  {rel_path} (git hook - needs git context)")
                self.results.append((str(rel_path), False, "SKIP: git hook", 0))
        
        # Try template-generator with demo args
        if self.arg_examples:
            print(f"\nRunning argument-dependent examples with demo args:")
            for file_path in sorted(self.arg_examples):
                self._run_with_args(file_path)
    
    def _run_example(self, file_path: Path):
        """Run a single example."""
        rel_path = file_path.relative_to(self.examples_dir)
        print(f"  {rel_path}...", end=" ", flush=True)
        
        start = time.time()
        success, status = self.run_python_file(file_path)
        elapsed = time.time() - start
        
        icon = "✅" if success else "❌"
        print(f"{icon} ({elapsed:.1f}s)")
        
        if not success:
            print(f"     Error: {status}")
        
        self.results.append((str(rel_path), success, status, elapsed))
    
    def _run_with_args(self, file_path: Path):
        """Run example with demo arguments."""
        rel_path = file_path.relative_to(self.examples_dir)
        print(f"  {rel_path} (with demo args)...", end=" ", flush=True)
        
        # Run with demo arguments
        start = time.time()
        try:
            result = subprocess.run(
                [sys.executable, str(file_path), "python", "demo-project",
                 "--description", "Demo project for testing",
                 "--author", "Test", "--email", "test@test.com"],
                capture_output=True,
                text=True,
                timeout=10,
                cwd=str(file_path.parent)
            )
            
            elapsed = time.time() - start
            success = result.returncode == 0
            status = "SUCCESS" if success else result.stderr[:100]
            
        except Exception as e:
            elapsed = time.time() - start
            success = False
            status = str(e)[:100]
        
        icon = "✅" if success else "❌"
        print(f"{icon} ({elapsed:.1f}s)")
        
        if not success:
            print(f"     Error: {status}")
        
        self.results.append((str(rel_path), success, status, elapsed))
    
    def print_summary(self):
        """Print final summary."""
        print("\n" + "=" * 70)
        print("EXAMPLE RUN SUMMARY")
        print("=" * 70)
        
        passed = sum(1 for _, success, _, _ in self.results if success)
        failed = len(self.results) - passed
        total_time = sum(t for _, _, _, t in self.results)
        
        print(f"\nTotal: {len(self.results)} examples")
        print(f"  ✅ Passed: {passed}")
        print(f"  ❌ Failed: {failed}")
        print(f"  ⏱️  Total time: {total_time:.1f}s")
        
        if failed > 0:
            print("\nFailed examples:")
            for path, success, status, _ in self.results:
                if not success:
                    print(f"  ❌ {path}: {status}")
        
        print("\n" + "=" * 70)
        return failed == 0


def main():
    """Run all examples."""
    examples_dir = Path(__file__).parent
    
    print("=" * 70)
    print("RUNNING ALL EXAMPLES")
    print("=" * 70)
    print(f"Examples directory: {examples_dir}")
    print()
    
    runner = ExampleRunner(examples_dir)
    runner.run_all()
    success = runner.print_summary()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
