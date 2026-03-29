# Goal Examples

This directory contains example configurations, workflows, and API usage for Goal.

## Directory Structure

```
examples/
├── README.md                    # This file
├── api-usage/                   # Python API examples
│   ├── README.md
│   ├── 01_basic_api.py
│   ├── 02_git_operations.py
│   ├── 03_commit_generation.py
│   ├── 04_version_validation.py
│   └── 05_programmatic_workflow.py
├── advanced-workflows/         # Complex workflows
│   ├── README.md
│   ├── hotfix-workflow.md
│   └── feature-branch.md
├── monorepo/                   # Multi-package repos
│   └── README.md
├── custom-hooks/               # Plugins and hooks
│   └── README.md
├── python-package/             # Python project example
│   └── pyproject.toml
├── nodejs-app/                 # Node.js project example
│   └── package.json
├── rust-crate/                 # Rust project example
│   └── Cargo.toml
├── makefile/                   # Makefile integration
│   └── Makefile
├── github-actions/             # CI/CD workflows
│   └── .github/workflows/
│       └── release.yml
├── enhanced-summary/           # Commit message examples
│   ├── README.md
│   ├── before-after.md
│   └── config-example.yaml
├── git-hooks/                  # Git hooks setup
│   ├── install.sh
│   └── prepare-commit-msg
├── license-management/         # License handling
│   └── README.md
├── multi-author/               # Team collaboration
│   └── README.md
├── wizard-setup/               # Interactive setup
│   └── README.md
└── markdown-demo.sh            # Demo script
```

## Usage Examples

### 1. Python API Usage

```bash
cd examples/api-usage
python 01_basic_api.py
python 02_git_operations.py
python 03_commit_generation.py
python 04_version_validation.py
python 05_programmatic_workflow.py
```

These examples demonstrate:
- Project detection and configuration
- Git operations (staging, diff, stats)
- Smart commit message generation
- Version validation across registries
- Full programmatic workflows

### 2. Advanced Workflows

```bash
# Hotfix workflow
cat examples/advanced-workflows/hotfix-workflow.md

# Feature branch workflow
cat examples/advanced-workflows/feature-branch.md

# Monorepo setup
cat examples/monorepo/README.md

# Custom hooks
cat examples/custom-hooks/README.md
```

### 3. Python Package

```bash
cd examples/python-package
goal init
goal --all
```

This example shows a typical Python package structure with:
- `pyproject.toml` for modern Python packaging
- pytest configuration for testing
- build and twine for publishing to PyPI

### 4. Node.js Application

```bash
cd examples/nodejs-app
goal init
goal push --yes --bump minor
```

This example demonstrates:
- `package.json` with npm scripts
- Jest for testing
- npm publish for distribution

### 5. Rust Crate

```bash
cd examples/rust-crate
goal init
goal --all
```

Features shown:
- `Cargo.toml` configuration
- Cargo test for testing
- Cargo publish for crates.io

### 6. Makefile Integration

```bash
cd examples/makefile
make help      # Show available targets
make release   # Interactive release
make patch     # Automatic patch release
make all       # Full automation with goal --all
```

The Makefile example includes:
- Development targets (test, lint, format)
- Release targets (patch, minor, major)
- CI/CD helper targets

### 7. GitHub Actions

The GitHub Actions workflow demonstrates:
- Automated testing on multiple Python versions
- Automatic releases on main branch push
- Manual releases with workflow dispatch
- Docker image building and publishing
- PyPI publishing

## Common Patterns

### Interactive Development

```bash
# Make changes
git add .
goal  # Interactive prompts for each stage
```

### Full Automation

```bash
# Automate everything
goal --all
# or
goal -a

# With specific version bump
goal --all --bump minor
```

### CI/CD Integration

```yaml
# GitHub Actions
- name: Release
  run: goal push --yes --bump patch

# Makefile in CI
make ci-release
```

### Custom Workflows

```bash
# Skip tests for docs
goal push --yes -m "docs: update README"

# Dry run to check
goal push --dry-run

# Custom commit message
goal push -m "feat: add new feature"

# Split commits by type
goal push --split --yes
```

### API Integration

```python
from goal.push.core import execute_push_workflow

ctx_obj = {'yes': True, 'markdown': False}
execute_push_workflow(
    ctx_obj=ctx_obj,
    bump='patch',
    dry_run=True,  # Safety first
    yes=True
)
```

### Custom Validators

```python
from goal.validators import validate_staged_files

# Add custom validation
def my_validator():
    try:
        validate_staged_files(config)
        return True
    except Exception as e:
        print(f"Validation failed: {e}")
        return False
```

## Best Practices

1. **Always use `goal init`** when starting a new project
2. **Use `--dry-run`** to preview changes before releasing
3. **Configure CI/CD** to use `goal push --yes` for automation
4. **Use semantic versioning** with appropriate bump types
5. **Keep tests fast** so they don't block releases
6. **Authenticate before publishing** to package registries
7. **Use conventional commits** with scopes for clarity
8. **Document with examples** in your project's examples/ directory

## Troubleshooting

### Tests Fail

```bash
# Run tests manually first
pytest
npm test
cargo test

# Then release with confidence
goal --all
```

### Publish Fails

```bash
# Check authentication
twine check
npm whoami
cargo login

# Retry publishing
goal push --yes
```

### Git Issues

```bash
# Check git status
goal status

# Ensure clean working directory
git add .
goal push
```

### API Import Errors

```bash
# Set PYTHONPATH
export PYTHONPATH="/path/to/goal:$PYTHONPATH"

# Or install in dev mode
pip install -e /path/to/goal
```

### Hook Not Running

```bash
# Check permissions
chmod +x .goal/hooks/*.py

# Verify path in goal.yaml
goal config show
```

## Contributing

To add new examples:

1. Create directory: `examples/my-example/`
2. Add README.md with description
3. Add working code/config files
4. Update this README
5. Test all commands work

## See Also

- [Main Documentation](../docs/README.md)
- [API Reference](../docs/api.md)
- [Configuration Guide](../docs/configuration.md)
