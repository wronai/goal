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
│   ├── 05_programmatic_workflow.py
│   └── test_integration.py
├── advanced-workflows/         # Complex workflows
├── configurations/             # Configuration examples
├── custom-hooks/               # Plugins and hooks
├── docker-integration/         # Docker examples
├── dotnet-project/             # .NET project example
├── enhanced-summary/           # Commit message examples
├── git-hooks/                  # Git hooks setup
├── github-actions/             # CI/CD workflows
├── gitlab-ci/                  # GitLab CI examples
├── go-project/                 # Go project example
├── java-project/               # Java project example
├── license-management/         # License handling
├── makefile/                   # Makefile integration
├── monorepo/                   # Multi-package repos
├── multi-author/               # Team collaboration
├── my-new-project/             # Template output example
├── nodejs-app/                 # Node.js project example
├── performance/                # Performance testing
├── php-project/                # PHP project example
├── python-package/             # Python project example
├── ruby-project/               # Ruby project example
├── rust-crate/                 # Rust project example
├── template-generator/         # Project scaffolding
├── testing/                    # Testing patterns
├── testing-guide/              # Testing documentation
├── validation/                 # Example validation tests
├── webhooks/                   # Webhook integrations
└── wizard-setup/               # Interactive setup
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

### 2. Advanced Workflows & CI/CD

```bash
# Advanced workflows
cat examples/advanced-workflows/README.md

# Monorepo setup
cat examples/monorepo/README.md

# Custom hooks
cat examples/custom-hooks/README.md

# GitHub Actions
cat examples/github-actions/.github/workflows/*.yml

# GitLab CI
cat examples/gitlab-ci/README.md

# Docker
cat examples/docker-integration/README.md
```

### 3. Testing & Validation

```bash
# Testing patterns
cd examples/testing
python 01_duplicate_call_detection.py

# Example validation
cd examples/validation
python run_all_validation.py

# Performance testing
cat examples/performance/README.md
```

### 4. Project Type Examples

```bash
# Python
cd examples/python-package

# Node.js
cd examples/nodejs-app

# Rust
cd examples/rust-crate

# Go
cd examples/go-project

# Java
cd examples/java-project

# .NET
cd examples/dotnet-project

# PHP
cd examples/php-project

# Ruby
cd examples/ruby-project
```

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
    dry_run=True,
    yes=True
)
```

### Webhook Integration

```bash
# Discord webhook
python examples/webhooks/discord-webhook.py "Release v1.0.0"

# Slack webhook
python examples/webhooks/slack-webhook.py "Release v1.0.0"
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
