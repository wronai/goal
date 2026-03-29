# Advanced Workflows for Goal

This directory contains advanced workflow examples for complex use cases.

## Examples

### 1. Monorepo Release (`monorepo-release/`)

Multi-package repository with coordinated releases.

```bash
cd examples/advanced-workflows/monorepo-release
goal --all  # Releases all packages with same version
```

### 2. Hotfix Workflow (`hotfix-workflow.md`)

Emergency patch release process.

```bash
# Critical security fix
goal push --yes --no-test --no-version-sync \
  -m "hotfix: patch CVE-2024-XXXX"

# Follow-up proper release
goal push --bump patch -m "release: v1.2.1 with security fix"
```

### 3. Feature Branch Workflow (`feature-branch.md`)

Development workflow with feature branches.

```bash
# On feature branch
goal push --yes --no-tag --no-publish

# After merge to main
goal push --bump minor --yes
```

### 4. Release Candidate Workflow (`release-candidate.md`)

Pre-release versioning strategy.

```bash
# Create RC
goal push --bump patch -m "release: v2.0.0-rc1"

# Promote to stable
goal push --bump patch -m "release: v2.0.0 stable"
```

### 5. Nightly Build Automation (`nightly-build.md`)

Automated nightly builds with CI/CD.

```yaml
# .github/workflows/nightly.yml
- name: Nightly Build
  run: goal --all --bump patch --yes
```

### 6. Multi-Environment Deployment (`multi-env.md`)

Deploy to staging then production.

```bash
# Staging
goal push --yes --no-publish

# Production (after testing)
goal publish
```

## Common Patterns

### Split Commits by Type

```bash
goal push --split --yes
```

Creates separate commits:
- `docs:` - Documentation changes
- `feat:` - New features  
- `test:` - Test additions
- `chore:` - Dependencies/CI

### Ticket Integration

```bash
# With TICKET file
echo "prefix=ABC-123" > TICKET
goal push --split

# Manual override
goal push --ticket "PROJ-456"
```

### Custom Commit Messages

```bash
# Override generated message
goal push -m "feat(api): implement OAuth2"

# With body from file
goal push -m "feat: new feature" --body-file changes.txt
```

## See Also

- [Basic Examples](../python-package/)
- [API Usage](../api-usage/)
- [CI/CD Integration](../github-actions/)
