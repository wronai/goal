# API Usage Examples for Goal

This directory contains examples showing how to use Goal programmatically via its Python API.

## Examples

### 1. Basic API Usage (`basic_api.py`)

```python
"""Basic API usage example."""
from goal.cli import push
from goal.project_bootstrap import bootstrap_project
from goal.doctor.core import diagnose_and_report

# Bootstrap a project
result = bootstrap_project(Path("."), "python", yes=True)
print(f"Environment OK: {result['env_ok']}")

# Diagnose project
report = diagnose_and_report(Path("."), "python", auto_fix=True)
print(f"Issues found: {len(report.issues)}")
```

### 2. Custom Commit Generator (`custom_commit.py`)

```python
"""Custom commit message generation."""
from goal.push.stages import get_commit_message
from goal.git_ops import get_staged_files, get_diff_content

# Get staged files
files = get_staged_files()
diff = get_diff_content()

# Generate commit message
ctx_obj = {'yes': True, 'markdown': False}
title, body, result = get_commit_message(
    ctx_obj, files, diff, message=None, ticket=None, abstraction="detailed"
)
print(f"Commit: {title}")
```

### 3. Version Management (`version_management.py`)

```python
"""Version synchronization example."""
from goal.version_validation import validate_project_versions
from goal.cli.version import get_current_version

# Get current version
version = get_current_version()

# Validate across registries
results = validate_project_versions(["python"], version)
for ptype, result in results.items():
    print(f"{ptype}: {result['local_version']} (registry: {result.get('registry_version')})")
```

### 4. Custom Validators (`custom_validators.py`)

```python
"""Custom validation before commit."""
from goal.validators import validate_staged_files
from goal.config.manager import Config

# Load config
config = Config.load("goal.yaml")

# Validate files
try:
    validate_staged_files(config)
    print("✓ All validations passed")
except Exception as e:
    print(f"✗ Validation failed: {e}")
```

### 5. Git Operations (`git_operations.py`)

```python
"""Direct git operations via Goal API."""
from goal.git_ops import (
    run_git, get_staged_files, get_diff_stats,
    get_remote_branch, push_to_remote
)

# Stage files
run_git('add', '-A')

# Get stats
stats = get_diff_stats()
print(f"Changed files: {len(stats)}")

# Push
branch = get_remote_branch()
push_to_remote(branch, "v1.0.0", no_tag=False, yes=True)
```

### 6. Configuration Management (`config_management.py`)

```python
"""Configuration management example."""
from goal.config import ensure_config, get_user_config
from goal.config.constants import DEFAULT_CONFIG

# Ensure project config
project_config = ensure_config()
print(f"Project name: {project_config.project.name}")

# Get user config
user = get_user_config()
print(f"Author: {user.get('author_name')}")

# Access constants
print(f"Default version: {DEFAULT_CONFIG['versioning']['initial_version']}")
```

### 7. Programmatic Workflow (`programmatic_workflow.py`)

```python
"""Complete programmatic workflow."""
import sys
from pathlib import Path

# Add goal to path if needed
sys.path.insert(0, "/path/to/goal")

from goal.push.core import execute_push_workflow

# Create context
ctx_obj = {
    'yes': True,
    'markdown': False,
    'config': None,
    'user_config': {'author_name': 'Developer'}
}

# Execute workflow
execute_push_workflow(
    ctx_obj=ctx_obj,
    bump='patch',
    no_tag=False,
    no_changelog=False,
    no_version_sync=False,
    message=None,
    dry_run=False,
    yes=True,
    markdown=False,
    split=False,
    ticket=None,
    abstraction=None,
    todo=False,
    force=False
)
```

### 8. Hook Integration (`hook_integration.py`)

```python
"""Custom pre-commit hook."""
from goal.hooks.manager import HooksManager
from goal.validators import validate_staged_files

def custom_pre_commit_hook():
    """Run custom validations before commit."""
    # Run standard validations
    validate_staged_files()
    
    # Add custom checks
    manager = HooksManager()
    manager.run_validation()
    
    return True

if __name__ == "__main__":
    if custom_pre_commit_hook():
        print("✓ Pre-commit checks passed")
        sys.exit(0)
    else:
        print("✗ Pre-commit checks failed")
        sys.exit(1)
```

### 9. Multi-Project Bootstrap (`multi_project_bootstrap.py`)

```python
"""Bootstrap multiple projects."""
from goal.project_bootstrap import bootstrap_all_projects

# Bootstrap all projects in monorepo
results = bootstrap_all_projects(root=Path("."), yes=True)

for result in results:
    print(f"Project: {result['project_type']}")
    print(f"  Env OK: {result['env_ok']}")
    print(f"  Tests: {len(result['tests_found'])}")
```

### 10. Custom Formatter (`custom_formatter.py`)

```python
"""Custom output formatting."""
from goal.formatter import format_push_result

# Format custom result
output = format_push_result(
    project_types=["python"],
    files=["src/main.py"],
    stats={"src/main.py": (10, 5)},
    current_version="1.0.0",
    new_version="1.0.1",
    commit_msg="fix: bug fix",
    commit_body="Detailed description",
    test_result="Passed",
    test_exit_code=0,
    actions=["Committed", "Tagged", "Pushed"]
)
print(output)
```

## Running Examples

```bash
# Set up Python path
export PYTHONPATH="/path/to/goal:$PYTHONPATH"

# Run example
python examples/api-usage/basic_api.py
```

## See Also

- [API Reference](../../docs/api.md)
- [Configuration Guide](../../docs/configuration.md)
- [Python API Examples](https://github.com/wronai/goal/tree/main/examples/api-usage)
