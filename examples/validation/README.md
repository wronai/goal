# Example Validation Framework

Framework for testing examples in the Goal project to catch common issues.

## Quick Start

```bash
# Run all validation tests
cd examples/validation
python run_all_validation.py

# Or run individual tests
python test_syntax_check.py
python test_imports.py
python test_api_signatures.py
python test_readme_consistency.py
```

## What It Tests

### 1. Syntax Check (`test_syntax_check.py`)
- **Python syntax** - All `.py` files compile correctly
- **Shell syntax** - All `.sh` files pass `bash -n`
- **JSON validity** - All `.json` files are valid JSON
- **YAML validity** - All `.yaml`/`.yml` files are valid YAML

### 2. Import Validation (`test_imports.py`)
- All `import goal.x` statements work
- All `from goal.x import y` statements work
- Imported modules and functions actually exist
- Catches broken imports after refactoring

### 3. API Signature Check (`test_api_signatures.py`)
- Function calls match actual API signatures
- No removed/renamed parameters are used
- Catches API changes that break examples

### 4. README Consistency (`test_readme_consistency.py`)
- All referenced files in READMEs exist
- All directories mentioned exist
- No broken markdown links
- New examples are documented

## CI Integration

Add to your CI pipeline:

```yaml
# .github/workflows/ci.yml
- name: Validate Examples
  run: |
    cd examples/validation
    python run_all_validation.py
```

## Exit Codes

- `0` - All tests passed
- `1` - One or more tests failed

## Adding New Validators

1. Create new test file: `test_my_validator.py`
2. Implement validator class
3. Add to `run_all_validation.py` test list

Example template:

```python
#!/usr/bin/env python3
"""My custom validator."""

import sys
from pathlib import Path

class MyValidator:
    def __init__(self, goal_root: Path):
        self.goal_root = goal_root
        self.errors = []
    
    def validate_all(self) -> bool:
        # Your validation logic
        return len(self.errors) == 0
    
    def print_report(self):
        # Print your report
        pass

def main():
    script_dir = Path(__file__).parent
    goal_root = script_dir.parent.parent
    
    validator = MyValidator(goal_root)
    valid = validator.validate_all()
    validator.print_report()
    
    sys.exit(0 if valid else 1)

if __name__ == "__main__":
    main()
```

## Common Issues Detected

### Import Errors
```
examples/api-usage/01_basic_api.py:
  🔴 [IMPORT] Cannot import goal.validators: No module named 'goal.validators'
```
**Fix**: Remove non-existent import or create the module.

### API Signature Mismatch
```
examples/api-usage/03_commit_generation.py:
  🔴 [INVALID_PARAM] goal.push.stages.handle_single_commit() got unexpected keyword argument 'deprecated_param'
```
**Fix**: Update example to use new API signature.

### Missing File References
```
examples/README.md:
  🔴 [MISSING_REF] Referenced file/dir not found: 'python-package/'
```
**Fix**: Update README to match actual directory structure.

### Syntax Errors
```
examples/custom-hooks/pre-commit.py:
  🔴 [PYTHON_SYNTAX] invalid syntax (line 45)
```
**Fix**: Fix the syntax error in the file.

## Running in Goal Development

```bash
# After making changes to Goal API, validate all examples
python examples/validation/run_all_validation.py

# This ensures your changes don't break examples
```

## Troubleshooting

### Python path issues
If imports fail because goal isn't in path:
```bash
export PYTHONPATH="/path/to/goal:$PYTHONPATH"
python run_all_validation.py
```

### Missing dependencies
Some validators may need optional dependencies:
```bash
pip install pyyaml  # For YAML validation
```

## Related

- [Main Examples README](../README.md)
- [API Usage Examples](../api-usage/)
- [Testing Guide](../testing-guide/)
