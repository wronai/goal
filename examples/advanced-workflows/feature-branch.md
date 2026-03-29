# Feature Branch Workflow

Development workflow using feature branches with Goal.

## Branch Strategy

```
main (production)
  ↑
develop (integration)
  ↑
feature/* (features)
hotfix/* (emergency fixes)
```

## Daily Workflow

### 1. Start Feature

```bash
# Update main
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/user-auth

# Work on feature
# ... make changes ...
```

### 2. Commit to Feature Branch

```bash
# Stage changes
git add .

# Commit without publishing
goal push --yes --no-tag --no-publish

# Push to remote for collaboration
git push origin feature/user-auth
```

### 3. Sync with Main

```bash
# Get latest changes
git checkout main
git pull origin main

# Rebase feature
git checkout feature/user-auth
git rebase main

# Or merge
git merge main
```

### 4. Create Pull Request

```bash
# Push final changes
git push origin feature/user-auth

# Create PR (using GitHub CLI)
gh pr create --title "feat: user authentication" \
  --body "Implements OAuth2 authentication flow"
```

### 5. Merge and Release

```bash
# After PR merge on main
git checkout main
git pull origin main

# Full release
goal push --bump minor --yes
```

## Goal Flags for Feature Work

| Flag | Purpose |
|------|---------|
| `--no-tag` | Don't create release tags |
| `--no-publish` | Don't publish to registry |
| `--no-test` | Skip tests (run manually) |
| `--split` | Organize commits by type |

## Example: Complete Feature

```bash
# Day 1: Start feature
git checkout -b feature/api-v2

# Make changes
echo "# New API" > API_V2.md
goal push --yes --no-tag -m "docs: API v2 specification"

# Day 2: Implementation
# ... code ...
goal push --yes --no-tag -m "feat: implement API v2 endpoints"

# Day 3: Tests
# ... tests ...
goal push --yes --no-tag -m "test: add API v2 tests"

# Day 4: Polish
goal push --yes --no-tag --split

# Day 5: Merge and release
git checkout main
git merge feature/api-v2 --no-ff
goal push --bump minor --yes
```

## Best Practices

1. **Commit Often**: Use `--no-tag` for intermediate commits
2. **Write Tests**: Before merging to main
3. **Update Changelog**: Only on release, not feature
4. **Clean History**: Use `--split` for organized commits
5. **Version Bump**: Only when merging to main

## See Also

- [Hotfix Workflow](hotfix-workflow.md)
- [Release Candidates](release-candidate.md)
