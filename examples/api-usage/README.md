# API Usage Examples for Goal

This directory contains examples showing how to use Goal programmatically via its Python API.

## Available Examples

### 1. Basic API Usage (`01_basic_api.py`)

Demonstrates project detection, configuration loading, and diagnostics.

```bash
python 01_basic_api.py
```

Key APIs used:
- `goal.project_bootstrap.bootstrap_project`
- `goal.doctor.core.diagnose_and_report`
- `goal.cli.version.get_current_version`

### 2. Git Operations (`02_git_operations.py`)

Shows how to use Goal's Git API for staging, diffs, and stats.

```bash
python 02_git_operations.py
```

Key APIs used:
- `goal.git_ops.run_git`
- `goal.git_ops.get_staged_files`
- `goal.git_ops.get_diff_content`

### 3. Commit Generation (`03_commit_generation.py`)

Example of generating smart commit messages programmatically.

```bash
python 03_commit_generation.py
```

Key APIs used:
- `goal.generator.generate_smart_commit_message`
- `goal.git_ops.get_staged_files`

### 4. Version Validation (`04_version_validation.py`)

Validates versions across registries and checks README badges.

```bash
python 04_version_validation.py
```

Key APIs used:
- `goal.version_validation.validate_project_versions`
- `goal.cli.version.get_current_version`

### 5. Programmatic Workflow (`05_programmatic_workflow.py`)

Complete programmatic workflow example.

```bash
python 05_programmatic_workflow.py
```

Key APIs used:
- `goal.push.core.execute_push_workflow`

### 6. Integration Tests (`test_integration.py`)

Pytest-based integration tests demonstrating Goal API testing patterns.

```bash
pytest test_integration.py -v
```

## Running Examples

```bash
# Set up Python path
export PYTHONPATH="/path/to/goal:$PYTHONPATH"

# Run example
cd examples/api-usage
python 01_basic_api.py
```

## See Also

- [Main Documentation](../../docs/README.md)
- [Configuration Guide](../../docs/configuration.md)
- [Testing Examples](../testing/)
