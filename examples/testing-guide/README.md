# Testing Examples for Goal

Comprehensive testing patterns and examples.

## Table of Contents

1. [Unit Tests](#unit-tests)
2. [Integration Tests](#integration-tests)
3. [Mock Examples](#mock-examples)
4. [Fixture Examples](#fixture-examples)
5. [Parameterized Tests](#parameterized-tests)

## Unit Tests

### Testing Git Operations

```python
# tests/test_git_ops.py
import pytest
from unittest.mock import patch, MagicMock
from goal.git_ops import run_git, get_staged_files

def test_run_git_success():
    """Test successful git command execution."""
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout='success',
            stderr=''
        )
        
        result = run_git('status')
        assert result.returncode == 0

def test_get_staged_files():
    """Test getting staged files list."""
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout='file1.py\nfile2.py\n',
            stderr=''
        )
        
        files = get_staged_files()
        assert 'file1.py' in files
        assert 'file2.py' in files
```

### Testing Configuration

```python
# tests/test_config.py
import pytest
from pathlib import Path
from goal.config import ensure_config

def test_config_loading(tmp_path):
    """Test configuration loading."""
    # Create test config
    config_file = tmp_path / "goal.yaml"
    config_file.write_text("""
version: "1.0"
project:
  name: "test"
  type: "python"
""")
    
    with patch('pathlib.Path.cwd', return_value=tmp_path):
        config = ensure_config()
        assert config is not None

def test_invalid_config():
    """Test handling of invalid config."""
    with pytest.raises(Exception):
        # Should raise for invalid YAML
        parse_config("invalid: yaml: content: :")
```

## Integration Tests

### Full Workflow Test

```python
# tests/integration/test_workflow.py
import pytest
import tempfile
from pathlib import Path

def test_full_push_workflow():
    """Test complete push workflow."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_dir = Path(tmpdir)
        
        # Setup project
        setup_test_project(project_dir)
        
        # Run workflow in dry-run mode
        from goal.push.core import execute_push_workflow
        
        ctx_obj = {
            'yes': True,
            'markdown': False
        }
        
        execute_push_workflow(
            ctx_obj=ctx_obj,
            bump='patch',
            dry_run=True,  # Safety
            yes=True
        )
        
        # Verify results
        assert (project_dir / "VERSION").exists()
```

### API Integration Test

```python
# tests/integration/test_api.py
import pytest
from goal.project_bootstrap import bootstrap_project

def test_bootstrap_python_project(tmp_path):
    """Test bootstrapping Python project."""
    # Create Python project structure
    (tmp_path / "pyproject.toml").write_text("""
[project]
name = "test"
version = "0.1.0"
""")
    
    result = bootstrap_project(tmp_path, "python", yes=True)
    
    assert result['project_type'] == "python"
    assert 'env_ok' in result
```

## Mock Examples

### Mocking External Services

```python
# tests/test_external_services.py
from unittest.mock import patch, MagicMock

def test_pypi_version_check():
    """Test PyPI version checking with mocked API."""
    with patch('urllib.request.urlopen') as mock_urlopen:
        # Mock response
        mock_response = MagicMock()
        mock_response.read.return_value = b'{"info": {"version": "1.0.0"}}'
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        from goal.version_validation import get_pypi_version
        version = get_pypi_version("test-package")
        
        assert version == "1.0.0"

def test_slack_webhook():
    """Test Slack notification with mocked HTTP."""
    with patch('urllib.request.urlopen') as mock_urlopen:
        mock_urlopen.return_value.__enter__.return_value = MagicMock(
            status=200
        )
        
        from examples.webhooks.slack_webhook import send_slack_notification
        result = send_slack_notification("Test message")
        
        assert result is True
```

## Fixture Examples

### Reusable Fixtures

```python
# conftest.py
import pytest
import tempfile
from pathlib import Path

@pytest.fixture
def temp_project():
    """Create temporary project directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_dir = Path(tmpdir)
        
        # Create basic structure
        (project_dir / "src").mkdir()
        (project_dir / "tests").mkdir()
        
        yield project_dir

@pytest.fixture
def git_repo(temp_project):
    """Create git repository in temp project."""
    import subprocess
    subprocess.run(['git', 'init'], cwd=temp_project, capture_output=True)
    subprocess.run(
        ['git', 'config', 'user.email', 'test@test.com'],
        cwd=temp_project, capture_output=True
    )
    subprocess.run(
        ['git', 'config', 'user.name', 'Test'],
        cwd=temp_project, capture_output=True
    )
    
    return temp_project

@pytest.fixture
def python_project(git_repo):
    """Create Python project with pyproject.toml."""
    (git_repo / "pyproject.toml").write_text("""
[project]
name = "test-project"
version = "0.1.0"
""")
    
    return git_repo
```

### Using Fixtures

```python
# tests/test_with_fixtures.py
def test_detect_project_type(python_project):
    """Test project type detection."""
    from goal.cli.version import detect_project_types
    
    import os
    original_cwd = os.getcwd()
    try:
        os.chdir(python_project)
        types = detect_project_types()
        assert "python" in types
    finally:
        os.chdir(original_cwd)

def test_validate_staged_files(git_repo):
    """Test validation with fixtures."""
    from goal.validators import validate_staged_files
    
    # Create and stage test file
    test_file = git_repo / "test.py"
    test_file.write_text("print('hello')")
    
    import subprocess
    subprocess.run(['git', 'add', '.'], cwd=git_repo, capture_output=True)
    
    # Should pass validation
    assert validate_staged_files(None) is None  # No exception
```

## Parameterized Tests

### Testing Multiple Scenarios

```python
# tests/test_scenarios.py
import pytest

@pytest.mark.parametrize("project_type,config_file", [
    ("python", "pyproject.toml"),
    ("nodejs", "package.json"),
    ("rust", "Cargo.toml"),
    ("go", "go.mod"),
])
def test_project_detection(project_type, config_file, tmp_path):
    """Test detection of different project types."""
    from goal.cli.version import detect_project_types
    
    # Create config file
    (tmp_path / config_file).touch()
    
    import os
    original_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        types = detect_project_types()
        assert project_type in types
    finally:
        os.chdir(original_cwd)

@pytest.mark.parametrize("bump_type,expected", [
    ("patch", "0.1.1"),
    ("minor", "0.2.0"),
    ("major", "1.0.0"),
])
def test_version_bumping(bump_type, expected):
    """Test version bumping logic."""
    from goal.version import bump_version
    
    result = bump_version("0.1.0", bump_type)
    assert result == expected
```

## Testing Best Practices

### 1. Use Markers

```python
# Mark slow tests
@pytest.mark.slow
def test_full_integration():
    pass

# Mark tests requiring network
@pytest.mark.network
def test_pypi_api():
    pass

# Skip in CI
@pytest.mark.skipif(
    os.environ.get('CI'),
    reason="Skip in CI environment"
)
def test_local_only():
    pass
```

### 2. Use Warnings

```python
import warnings

def test_deprecated_feature():
    with pytest.warns(DeprecationWarning):
        # Test deprecated functionality
        old_function()
```

### 3. Test Output Capture

```python
def test_cli_output(capsys):
    """Test command-line output."""
    from goal.cli import main
    
    # Run command
    main(['--version'])
    
    # Capture output
    captured = capsys.readouterr()
    assert "Goal v" in captured.out
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=goal --cov-report=html

# Run specific test file
pytest tests/test_git_ops.py

# Run with markers
pytest -m "not slow"
pytest -m "integration"

# Run in parallel
pytest -n auto

# Debug mode
pytest --pdb

# Verbose output
pytest -v
```

## CI Integration

### GitHub Actions

```yaml
- name: Run tests
  run: pytest tests/ -v --cov=goal --cov-report=xml

- name: Upload coverage
  uses: codecov/codecov-action@v3
  with:
    file: ./coverage.xml
```

### Configuration

```ini
# pytest.ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
    network: marks tests requiring network
```

## See Also

- [Integration Tests in API Usage](../api-usage/test_integration.py)
- [Goal Testing Guide](../../docs/testing.md)
