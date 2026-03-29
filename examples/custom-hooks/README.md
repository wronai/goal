# Custom Plugins and Hooks

Extending Goal with custom functionality.

## Overview

Goal supports custom hooks at various stages of the workflow:

- Pre-commit hooks
- Post-commit hooks
- Pre-publish hooks
- Custom validators
- Output formatters

## Hook Locations

```
.my-project/
├── .goal/
│   ├── hooks/
│   │   ├── pre-commit.py    # Before commit
│   │   ├── post-commit.py   # After commit
│   │   ├── pre-push.py      # Before push
│   │   └── pre-publish.py   # Before publish
│   └── plugins/
│       └── custom_validator.py
└── goal.yaml               # Hook configuration
```

## Configuration

### goal.yaml

```yaml
version: "1.0"

advanced:
  hooks:
    pre-commit: ".goal/hooks/pre-commit.py"
    post-commit: ".goal/hooks/post-commit.py"
    pre-push: ".goal/hooks/pre-push.py"
    pre-publish: ".goal/hooks/pre-publish.py"
  
  validators:
    - "custom_security_check"
    - "custom_performance_check"
```

## Example Hooks

### Pre-Commit: Security Scan

```python
#!/usr/bin/env python3
"""Pre-commit hook: Security scan."""
import sys
import subprocess

def main():
    """Run security checks before commit."""
    # Check for secrets
    result = subprocess.run(
        ["git", "secrets", "--scan"],
        capture_output=True
    )
    
    if result.returncode != 0:
        print("❌ Security issues found!")
        print(result.stdout.decode())
        return 1
    
    print("✓ Security scan passed")
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

### Post-Commit: Notification

```python
#!/usr/bin/env python3
"""Post-commit hook: Send notification."""
import os
import requests

def main():
    """Send Slack notification after commit."""
    commit_msg = os.popen("git log -1 --pretty=%B").read().strip()
    
    webhook_url = os.environ.get("SLACK_WEBHOOK_URL")
    if not webhook_url:
        return 0
    
    payload = {
        "text": f"New commit: {commit_msg[:50]}..."
    }
    
    requests.post(webhook_url, json=payload)
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

### Pre-Publish: Test Registry

```python
#!/usr/bin/env python3
"""Pre-publish hook: Test package installation."""
import subprocess
import tempfile
import sys

def main():
    """Test package in clean environment before publishing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create clean venv
        result = subprocess.run(
            ["python", "-m", "venv", f"{tmpdir}/venv"],
            capture_output=True
        )
        
        if result.returncode != 0:
            print("❌ Failed to create test environment")
            return 1
        
        # Test install
        pip = f"{tmpdir}/venv/bin/pip"
        result = subprocess.run(
            [pip, "install", "dist/*.whl"],
            capture_output=True
        )
        
        if result.returncode != 0:
            print("❌ Package installation test failed")
            return 1
    
    print("✓ Package installation test passed")
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

## Custom Validators

### File Size Validator

```python
# .goal/plugins/file_size_validator.py
"""Custom validator: Check file sizes."""
from pathlib import Path

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def validate():
    """Check all staged files are under size limit."""
    import subprocess
    
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        capture_output=True, text=True
    )
    
    staged_files = result.stdout.strip().split("\n")
    
    for file_path in staged_files:
        path = Path(file_path)
        if path.exists():
            size = path.stat().st_size
            if size > MAX_FILE_SIZE:
                print(f"❌ {file_path}: {size / 1024 / 1024:.1f}MB > 10MB limit")
                return False
    
    return True
```

### Custom Commit Message Validator

```python
# .goal/plugins/commit_validator.py
"""Custom validator: Enforce commit message format."""
import re

COMMIT_PATTERN = re.compile(
    r"^(feat|fix|docs|style|refactor|test|chore)(\(.+\))?: .{10,100}$"
)

def validate(message: str) -> bool:
    """Validate commit message format."""
    if not COMMIT_PATTERN.match(message):
        print("❌ Invalid commit message format")
        print("Expected: type(scope): description (10-100 chars)")
        return False
    return True
```

## Programmatic Hook Registration

```python
# Register hooks programmatically
from goal.hooks.manager import HooksManager

manager = HooksManager()

# Register custom hook
@manager.pre_commit
def my_pre_commit_hook():
    """Custom pre-commit logic."""
    print("Running custom pre-commit check...")
    return True

# Register validator
@manager.validator
def my_validator(files):
    """Custom file validation."""
    for f in files:
        if f.endswith('.secret'):
            print(f"❌ Cannot commit secret files: {f}")
            return False
    return True
```

## Using Hooks Manager

```python
from goal.hooks.manager import HooksManager

def main():
    manager = HooksManager()
    
    # Run all pre-commit hooks
    if not manager.run_pre_commit():
        print("Pre-commit hooks failed")
        sys.exit(1)
    
    # Run all validators
    if not manager.run_validation():
        print("Validation failed")
        sys.exit(1)
    
    # Run post-commit hooks
    manager.run_post_commit()

if __name__ == "__main__":
    main()
```

## Best Practices

1. **Keep Hooks Fast**: < 5 seconds for pre-commit
2. **Fail Fast**: Exit non-zero on first error
3. **Clear Messages**: Print what failed and why
4. **Optional Hooks**: Allow skipping with env var
5. **Logging**: Log to `.goal/hooks.log`

## Installation

### Automated Setup

```bash
# Create hook directory
mkdir -p .goal/hooks

# Copy examples
curl -o .goal/hooks/pre-commit.py \
  https://raw.githubusercontent.com/wronai/goal/main/examples/custom-hooks/pre-commit.py

# Make executable
chmod +x .goal/hooks/pre-commit.py
```

### Goal Integration

```bash
# Enable hooks
goal config set hooks.pre-commit .goal/hooks/pre-commit.py

# Verify
goal doctor
```

## See Also

- [API Usage](../api-usage/)
- [Advanced Workflows](../advanced-workflows/)
